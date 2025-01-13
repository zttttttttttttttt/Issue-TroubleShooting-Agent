# planners/generic_planner.py

import json
from typing import List

from models.model_registry import ModelRegistry
from utils.logger import Logger
from config import Config


class Step:
    """
    Represents a step with a name and a description.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Step(name='{self.name}', description='{self.description}')"


class GenericPlanner:
    """
    A simple planner that calls the model to break a task into JSON steps.
    """

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


Output ONLY valid JSON. No extra text or markdown.
Steps:
"""

        response = self.model.process(prompt)
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
            if name and desc:
                results.append(Step(name=name, description=desc))
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
