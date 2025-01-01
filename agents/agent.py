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
            return "Task execution completed using planner."
        else:
            # Directly execute the task
            response = self._model.process(task)
            self.logger.info(f"Response: {response}")
            return response
