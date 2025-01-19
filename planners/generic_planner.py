# planners/generic_planner.py

import json
from typing import List, Optional

from langchain_core.tools import BaseTool

from models.model_registry import ModelRegistry
from utils.logger import get_logger
from config import Config


class Step:
    """
    Represents a step with a name and a description.
    """

    def __init__(self, name: str, description: str, use_tool: bool, tool_name: str):
        self.name = name
        self.description = description
        self.use_tool = use_tool
        self.tool_name = tool_name

    def __repr__(self):
        return (
            f"Step(name='{self.name}', description='{self.description}', "
            f"use_tool='{self.use_tool}', tool_name='{self.tool_name}')"
        )


class GenericPlanner:
    """
    A simple planner that calls the model to break a task into JSON steps.
    """

    DEFAULT_PROMPT = """\
We have the following knowledge that might help: {knowledge}

Given the following task and the possible tools, generate a detailed plan by breaking it down into actionable steps.
Present each step in JSON format with the attributes 'step_name', 'step_description', 'use_tool', and optionally 'tool_name'.
All steps should be encapsulated under the 'steps' key.

Example:
{example_json1}

{example_json2}

Task: {task}

Tools: {tools_knowledge}

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
            "tool_name": "Event"
        },
        ...
    ]
}"""

    EXAMPLE_JSON2 = """\
{
    "steps": [
        {
            "step_name": "Prepare eggs",
            "step_description": "Get the eggs from the fridge and put them on the table.",
            "use_tool": false
        },
        ...
    ]
}"""

    def __init__(
        self, model: str = None, log_level: Optional[str] = None, prompt: str = None
    ):
        """
        If 'model' is not provided, the default model from config will be used.
        'prompt' can override the default prompt used for planning.
        """
        self.logger = get_logger("generic-planner", log_level)
        if not model:
            model = Config.DEFAULT_MODEL

        self.model_name = model
        self.model = ModelRegistry.get_model(self.model_name)
        if not self.model:
            self.logger.error(f"Model '{self.model_name}' not found for planning.")
            raise ValueError(
                f"Model '{self.model_name}' is not supported for planning."
            )
        self.logger.info(f"GenericPlanner initialized with model: {self.model.name}")

        self._prompt = prompt or self.DEFAULT_PROMPT

    @property
    def prompt(self) -> str:
        """Get or set the single plan prompt (for dividing tasks into steps)."""
        return self._prompt

    @prompt.setter
    def prompt(self, value: str):
        self._prompt = value

    def plan(
        self, task: str, tools: Optional[List[BaseTool]], knowledge: str = ""
    ) -> List[Step]:
        """
        Use the LLM to break down the task into multiple steps in JSON format.
        'knowledge' is appended to the prompt to guide the planning process.
        """
        self.logger.info(f"Creating plan for task: {task}")
        tools_knowledge_list = []
        if tools is not None:
            tools_knowledge_list = [
                f"tool name: {tool.name}, tool description: {tool.description}"
                for tool in tools
            ]
        tools_knowledge_str = "\n".join(tools_knowledge_list)

        final_prompt = self._prompt.format(
            knowledge=knowledge,
            task=task,
            tools_knowledge=tools_knowledge_str,
            example_json1=self.EXAMPLE_JSON1,
            example_json2=self.EXAMPLE_JSON2,
        )

        response = self.model.process(final_prompt)
        response_text = str(response)

        if not response_text or not response_text.strip():
            self.logger.error("LLM returned an empty or null response.")
            raise ValueError("LLM returned an empty or null response.")

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

        # Convert steps_data to Step objects
        results = []
        for sd in steps_data:
            name = sd.get("step_name")
            desc = sd.get("step_description")
            use_tool = sd.get("use_tool")
            tool_name = sd.get("tool_name")
            if name and desc and use_tool:
                results.append(
                    Step(
                        name=name,
                        description=desc,
                        use_tool=use_tool,
                        tool_name=tool_name,
                    )
                )
            else:
                self.logger.warning(f"Incomplete step data: {sd}")

        self.logger.info(f"Got {len(results)} steps from the LLM.")
        return results

    def parse_steps(self, response: str) -> List[Step]:
        """
        Parse the LLM response to extract individual steps and return them as Step objects.

        Args:
            response (str): The raw response from the LLM.

        Returns:
            List[Step]: A list of Step objects extracted from the response.
        """
        self.logger.debug(f"Raw planner response: {response}")
        try:
            data = json.loads(response)
            steps_data = data.get("steps", [])
            steps = []
            for step in steps_data:
                step_name = step.get("step_name")
                step_description = step.get("step_description")
                if step_name and step_description:
                    steps.append(Step(name=step_name, description=step_description))
                else:
                    self.logger.warning(f"Incomplete step data: {step}")
            return steps
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError("Invalid JSON format received from the planner.")
        except Exception as e:
            self.logger.error(f"Unexpected error during parsing steps: {e}")
            raise
