from models.model_registry import ModelRegistry
from utils.logger import Logger
from typing import Optional, List
from planners import GenericPlanner, Step
from config import Config


class Agent:
    def __init__(self, model: Optional[str] = None):
        """
        If 'model' is not provided, the default model from config will be used.
        """
        self.logger = Logger()
        self._model = None
        self._planner = None

        # This list holds execution data for each step in sequence.
        # Example entry:
        # {
        #   "step_name": "Draw the stem",
        #   "step_description": "Draw a vertical line as the flower's stem",
        #   "step_result": "Stem drawn successfully."
        # }
        self._execution_history = []

        # If no model is passed, use the default from config
        if not model:
            model = Config.DEFAULT_MODEL

        # Use the property setter to initialize the model
        self.model = model

        self.logger.info("Agent instance created.")

    @property
    def model(self) -> Optional[str]:
        return self._model

    @model.setter
    def model(self, model_name: str):
        model = ModelRegistry.get_model(model_name)
        if not model:
            self.logger.error(f"Model '{model_name}' not found in registry.")
            raise ValueError(f"Model '{model_name}' is not supported.")
        self._model = model
        self.logger.info(f"Agent model set to: {model.name}")

    @property
    def planner(self) -> Optional[GenericPlanner]:
        return self._planner

    @planner.setter
    def planner(self, planner: GenericPlanner):
        if not isinstance(planner, GenericPlanner):
            self.logger.error("Planner must be an instance of GenericPlanner.")
            raise TypeError("Planner must be an instance of GenericPlanner.")
        self._planner = planner
        self.logger.info(f"Agent planner set to: {planner.__class__.__name__}")

    @property
    def execution_history(self) -> List[dict]:
        """
        Read-only access to the execution history.
        Each item is a dict with keys: 'step_name', 'step_description', 'step_result'.
        """
        return self._execution_history

    def execute(self, task: str):
        self.logger.info(f"Executing task: {task}")
        if self._planner:
            # Use planner to create a plan
            steps: List[Step] = self._planner.plan(task)
            self.logger.info(f"Executing plan with {len(steps)} steps.")
            for idx, step in enumerate(steps, 1):
                self.logger.info(f"Executing Step {idx}: {step.description}")
                response = self._model.process(step.description)
                self.logger.info(f"Response for Step {idx}: {response}")

                # Record the step execution
                self._execution_history.append(
                    {
                        "step_name": step.name,
                        "step_description": step.description,
                        "step_result": str(response),
                    }
                )

            return "Task execution completed using planner."
        else:
            # Directly execute the task
            response = self._model.process(task)
            self.logger.info(f"Response: {response}")

            self._execution_history.append(
                {
                    "step_name": "Direct Task Execution",
                    "step_description": task,
                    "step_result": str(response),
                }
            )

            return response

    def get_execution_result(self) -> str:
        """
        Produce an overall summary describing how the solution was completed,
        using the LLM to format the final explanation.

        Returns:
            A string representing the summary or conclusion of the entire execution.
        """

        # Build a textual representation of the execution history
        history_lines = []
        for idx, record in enumerate(self._execution_history, 1):
            line = (
                f"Step {idx}: {record['step_name']}\n"
                f"Description: {record['step_description']}\n"
                f"Result: {record['step_result']}\n"
            )
            history_lines.append(line)

        history_text = "\n".join(history_lines)

        # Construct a prompt for summarizing the entire execution
        prompt = f"""
You are an assistant summarizing the outcome of a multi-step plan execution.
Below is the complete step-by-step execution history. Provide a concise,
well-structured summary describing how the solution was achieved and any
notable details. Include each step's role in the final outcome.

Execution History:
{history_text}

Summary:
"""

        self.logger.info("Generating final execution result (summary).")
        summary_response = self._model.process(request=prompt)

        # If the model returns an AIMessage, extract text if needed
        if hasattr(summary_response, "content"):
            return summary_response.content
        else:
            return str(summary_response)
