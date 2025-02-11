# models/base_model.py

from abc import ABC, abstractmethod

from agent_core.config import Environment

Environment()


class BaseModel(ABC):
    def __init__(self):
        self.name = self.name()

    @abstractmethod
    def process(self, command: str) -> str:
        pass

    @abstractmethod
    def name(self) -> str:
        pass
