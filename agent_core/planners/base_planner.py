# planners/base_planner.py

from abc import ABC, abstractmethod
from typing import List, Optional

from langchain_core.tools import BaseTool

from agent_core.entities.steps import Steps


class BasePlanner(ABC):
    """
    An abstract base class for all planners.
    Both GenericPlanner and GraphPlanner will inherit from this.
    """

    @abstractmethod
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
        Generates a plan (list of Steps, or node-based structure, etc.) from the LLM.
        """
        pass

    @abstractmethod
    def execute_plan(
        self,
        *args,  # used to allow flexible signatures in child classes
        **kwargs,
    ):
        """
        Executes the already-generated plan (steps or node graph).
        """
        pass