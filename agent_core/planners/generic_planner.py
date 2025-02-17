# planners/generic_planner.py

import json
from typing import List, Optional, Dict
from langchain_core.tools import BaseTool
from .base_planner import BasePlanner, tool_knowledge_format, background_format
from ..entities.steps import Steps, Step
from ..evaluators import BaseEvaluator
from ..utils.context_manager import ContextManager


class GenericPlanner(BasePlanner):
    """
    A simple planner that calls the model to break a task into JSON steps.
    Each step may optionally specify a category, used for specialized evaluation.
    """

    EXAMPLE_JSON1 = """
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

    EXAMPLE_JSON2 = """
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

    def __init__(self, model_name: str = None, log_level: Optional[str] = None):
        """
        If 'model' is not provided, the default model from config will be used.
        'prompt' can override the default prompt used for planning.
        """
        super().__init__(model_name, log_level)

    def plan(
        self,
        task: str,
        tools: Optional[List[BaseTool]],
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

        tools_knowledge = tool_knowledge_format(tools)
        categories_str = ", ".join(categories) if categories else "(Not defined)"

        final_prompt = self.prompt.format(
            knowledge=knowledge,
            background=background_format(background),
            task=task,
            tools_knowledge=tools_knowledge,
            example_json1=self.EXAMPLE_JSON1,
            example_json2=self.EXAMPLE_JSON2,
            categories_str=categories_str,
        )

        response = self._model.process(final_prompt)
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

        plan = self.analyse_result(steps_data, categories)
        self.logger.info(f"Got {len(plan.steps)} steps from the LLM.")
        return plan

    def execute_plan(
        self,
        plan: Steps,
        task: str,
        execution_history: Steps,
        evaluators_enabled: bool,
        evaluators: dict,
        context_manager=None,
        background: str = "",
    ):
        """
        Execute a list of steps (previously planned).
        This replaces the step-by-step logic that was inside agent.py for GenericPlanner.
        """
        self.logger.info(f"Executing plan with {len(plan.steps)} steps.")

        for idx, step in enumerate(plan.steps, 1):
            context_section = (
                context_manager.context_to_str() if context_manager else ""
            )
            final_prompt = f"""
                {context_section}
                {background_format(background)}
                <Task>
                <Root Task>
                {task}
                </Root Task>
                {step.description}
                </Task>
                """

            self.logger.info(f"Executing Step {idx}: {step.description}")
            response = self._model.process(final_prompt)
            self.logger.info(f"Response for Step {idx}: {response}")

            # Optional Evaluation
            if evaluators_enabled:
                self.process_evaluator(
                    task, step, evaluators, response, background, context_manager
                )

            # Record the step execution
            execution_history.add_step(
                Step(name=step.name, description=step.description, result=str(response))
            )
            context_manager.add_context(
                "Execution History",
                execution_history.execution_history_to_str(),
            )
        return "Task execution completed using GenericPlanner."

    def process_evaluator(
        self,
        root_task: str,
        step: Step,
        evaluators: Dict[str, BaseEvaluator],
        response: str,
        background: str,
        context_manager: ContextManager,
    ):
        chosen_cat = step.category if step.category in evaluators else "default"
        evaluator = evaluators.get(chosen_cat)
        if evaluator:
            evaluator_result = evaluator.evaluate(
                root_task, step.description, response, background, context_manager
            )
            self.logger.info(
                f"Evaluator Decision: {evaluator_result.decision}, Score: {evaluator_result.score}"
            )
        else:
            self.logger.warning(
                f"No evaluator found even for 'default' category. Skipping evaluation."
            )

    def analyse_result(self, steps_data, categories):
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
                    category=final_cat,
                )
                plan.add_step(step)
            else:
                self.logger.warning(f"Incomplete step data: {sd}")
        return plan
