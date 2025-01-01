import json
from models.model_registry import ModelRegistry
from utils.logger import Logger
from typing import List
from .step import Step
from config import Config


class GenericPlanner:
    def __init__(self, model: str = None):
        """
        If 'model' is not provided, the default model from config will be used.
        """
        self.logger = Logger()
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

    def plan(self, task: str) -> List[Step]:
        """
        Use the LLM to break down the task into multiple steps in JSON format.

        Args:
            task (str): The task to be broken down.

        Returns:
            List[Step]: A list of Step objects to execute the task.
        """
        self.logger.info(f"Creating plan for task: {task}")
        prompt = f"""
Given the following task, generate a detailed plan by breaking it down into actionable steps. Present each step in JSON format with the attributes 'step_name' and 'step_description'. All steps should be encapsulated under the 'steps' key.

Example:
{{
    "steps": [
        {{
            "step_name": "Prepare eggs",
            "step_description": "Get the eggs from the fridge and put them on the table."
        }},
        ...
    ]
}}

Task: {task}

Steps:
"""
        try:
            response = self.model.process(request=prompt)
            # Extract the textual content from the AIMessage object
            if hasattr(response, "content"):
                response_text = response.content
            elif hasattr(response, "text"):
                response_text = response.text
            else:
                # Fallback if neither attribute exists
                response_text = str(response)

            steps = self.parse_steps(response_text)
            self.logger.info(f"Plan created with {len(steps)} steps.")
            return steps
        except Exception as e:
            self.logger.error(f"Error during planning: {e}")
            raise

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
