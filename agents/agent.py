from models.model_registry import ModelRegistry
from utils.logger import Logger


class Agent:
    def __init__(self, model: str):
        self.logger = Logger()
        self.model = ModelRegistry.get_model(model)
        if not self.model:
            self.logger.error(f"Model '{model}' not found in registry.")
            raise ValueError(f"Model '{model}' is not supported.")
        self.logger.info(f"Agent initialized with model: {self.model.name}")

    def execute(self, request: str):
        self.logger.info(f"Executing command: {request}")
        response = self.model.process(request)
        self.logger.info(f"Response: {response}")
        return response
