# planners/generic_planner.py

import json
from typing import List, Optional
import os
from langchain_core.tools import BaseTool

from agent_core.models.model_registry import ModelRegistry
from agent_core.utils.logger import get_logger
from .base_planner import BasePlanner
from ..entities.steps import Steps, Step
from ..utils.llm_chat import LLMChat


class GenericPlanner(BasePlanner):
    """
    A simple planner that calls the model to break a task into JSON steps.
    Each step may optionally specify a category, used for specialized validation.
    """

    DEFAULT_PROMPT = """ 
Given the following task and the possible tools, generate a plan based on provided knowledge by breaking it down into actionable steps.

**Instructions for generating 'use_tool':**
1) If the content between the <Tools></Tools> is empty, you MUST set "use_tool" to false for every step, and omit the "tool_name" key.
2) If the <Tools></Tools> area has content, you MAY set "use_tool" to true when appropriate. 
   - If "use_tool" is true, be sure to include "tool_name" in that step.
   - Also ensure "step_description" references any necessary tool properties or arguments.

**Task Breakdown Requirements:**
1) All steps should be encapsulated under the "steps" key in valid JSON.
2) Present each step in JSON format with the attributes:
  "step_name", "step_description", "use_tool", optionally "tool_name", and "step_category".
3) The possible categories for each step are: {categories_str}.
  If you cannot fit into any existing category, define a new category in "step_category".
4) Output **ONLY** valid JSON. No extra text, no Markdown.

<Knowledge>
{knowledge}
</Knowledge>

<Examples>
{example_json1}
{example_json2}
</Examples>

<Tools>
{tools_knowledge}
</Tools>

<Task>
{task}
</Task>

Output ONLY valid JSON. No extra text or markdown.
Steps:
"""

    EXAMPLE_JSON1 = """\
{
    "steps": [
        {
            "step_name": "Prepare eggs",
            "step_description": "Get the eggs from the fridge and put them on the table.",
            "use_tool": true,
            "tool_name": "Event",
            "step_category": "action"
        },
        ...
    ]
}"""

    EXAMPLE_JSON2 = """\
{
    "steps": [
        {
            "step_name": "Plan code structure",
            "step_description": "Outline the classes and methods.",
            "use_tool": false,
            "step_category": "coding"
        },
        ...
    ]
}"""

    def __init__(
        self, model_name: str = None, log_level: Optional[str] = None
    ):
        """
        If 'model' is not provided, the default model from config will be used.
        'prompt' can override the default prompt used for planning.
        """
        self.logger = get_logger("generic-planner", log_level)
        self.model_name = model_name if model_name else os.getenv("DEFAULT_MODEL")
        self.model = ModelRegistry.get_model(self.model_name)
        self.logger.info(f"GenericPlanner initialized with model: {self.model.name}")
        self.prompt = self.DEFAULT_PROMPT

    def plan(
        self,
        task: str,
        tools: Optional[List[BaseTool]],
        execute_history: Steps,
        knowledge: str = "",
        background: str = "",
        categories: Optional[List[str]] = None,
    ) -> Steps:
        """
        Use the LLM to break down the task into multiple steps in JSON format.
        'knowledge' is appended to the prompt to guide the planning process.
        If 'categories' is provided, we pass it to the LLM so it can properly categorize each step.
        """
        self.logger.info(f"Creating plan for task: {task}")

        tools_knowledge_list = []
        if tools is not None:
            tools_knowledge_list = [
                str(tool.args_schema.model_json_schema()) for tool in tools
            ]
        tools_knowledge = "\n".join(tools_knowledge_list)

        categories_str = ", ".join(categories) if categories else "(Not defined)"

        final_prompt = self.prompt.format(
            knowledge=knowledge,
            task=task,
            tools_knowledge=tools_knowledge,
            example_json1=self.EXAMPLE_JSON1,
            example_json2=self.EXAMPLE_JSON2,
            categories_str=categories_str,
        )

        response = self.model.process(final_prompt)
        response_text = str(response)

        if not response_text or not response_text.strip():
            error_msg = "LLM returned an empty or null response."
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        self.logger.debug(f"Raw LLM response: {repr(response_text)}")

        # Minor cleanup of possible code fences
        cleaned = response_text.replace("```json", "").replace("```", "").strip()

        # Attempt JSON parse
        try:
            data = json.loads(cleaned)
            steps_data = data.get("steps", [])
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON: {e}")
            self.logger.error(f"Raw LLM response was: {cleaned}")
            raise ValueError("Invalid JSON format in planner response.")

        valid_categories = set(categories) if categories else set()

        # Convert steps_data to Step objects
        plan = Steps()
        for sd in steps_data:
            name = sd.get("step_name")
            desc = sd.get("step_description")
            use_tool = sd.get("use_tool")
            tool_name = sd.get("tool_name")
            raw_cat = sd.get("step_category", "default")

            # If LLM returned a category not in recognized set, fallback to 'default'
            final_cat = raw_cat if raw_cat in valid_categories else "default"

            if name and desc:
                step = Step(
                    name=name,
                    description=desc,
                    use_tool=use_tool,
                    tool_name=tool_name,
                    category=final_cat
                )
                plan.add_step(step)
            else:
                self.logger.warning(f"Incomplete step data: {sd}")

        self.logger.info(f"Got {len(plan.steps)} steps from the LLM.")
        return plan

    def execute_plan(
        self,
        plan: Steps,
        execution_history: Steps,
        validators_enabled: bool,
        validators: dict,
        context_manager=None,
        llm_chat: LLMChat = None,
        background: str = "",
    ):
        """
        Execute a list of steps (previously planned).
        This replaces the step-by-step logic that was inside agent.py for GenericPlanner.
        """
        self.logger.info(f"Executing plan with {len(plan.steps)} steps.")

        for idx, step in enumerate(plan.steps, 1):
            # Possibly incorporate the context in the step prompt
            if execution_history and context_manager:
                context_manager.add_context(
                    "Execution History",
                    execution_history.execution_history_to_str(),
                )
            context_section = (
                context_manager.context_to_str() if context_manager else ""
            )
            final_prompt = (
                f"{context_section}"
                f"{background_format(background)}"
                f"<Task>\n"
                f"{step.description}\n"
                f"</Task>\n"
            )

            self.logger.info(f"Executing Step {idx}: {step.description}")
            response = self.model.process(final_prompt)
            self.logger.info(f"Response for Step {idx}: {response}")

            # Optional validation
            if validators_enabled:
                chosen_cat = (
                    step.category if step.category in validators else "default"
                )
                validator = validators.get(chosen_cat)
                if validator:
                    decision, score, details = validator.validate(
                        step.description, response
                    )
                    self.logger.info(f"Validator Decision: {decision}, Score: {score}")
                else:
                    self.logger.warning(
                        f"No validator found even for 'default' category. Skipping validation."
                    )
            # Record the step execution
            step.result = str(response)
        return "Task execution completed using GenericPlanner."


def background_format(background: str):
    background_str = ""
    if background != "":
        background_str = f"<Background>\n{background}\n</Background>\n"
    return background_str