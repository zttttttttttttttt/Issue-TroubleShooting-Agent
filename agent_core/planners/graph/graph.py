from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from langchain_core.tools import BaseTool
from agent_core.utils.logger import get_logger


@dataclass
class ExecutionResult:
    output: str
    evaluation_score: float
    timestamp: datetime


@dataclass
class ReplanHistory:
    history: List[Dict] = field(default_factory=list)

    def add_record(self, record: Dict):
        self.history.append(record)


@dataclass
class Node:
    """
    Represents a single node in the PlanGraph.
    """

    id: str
    task_description: str
    next_nodes: List[str] = field(default_factory=list)

    task_use_tool: bool = False
    task_tool_name: str = ""
    task_tool: BaseTool = None

    execution_results: List[ExecutionResult] = field(default_factory=list)
    evaluation_threshold: float = 0.9
    max_attempts: int = 3
    current_attempts: int = 0
    failed_reasons: List[str] = field(default_factory=list)

    task_category: str = "default"

    def set_next_node(self, node: "Node"):
        if node.id not in self.next_nodes:
            self.next_nodes.append(node.id)


@dataclass
class PlanGraph:
    """
    Holds multiple Node objects in a directed structure.
    Node-based plan execution with possible replan logic.
    """

    logger = get_logger("plan-graph")

    nodes: Dict[str, Node] = field(default_factory=dict)
    start_node_id: Optional[str] = None
    replan_history: ReplanHistory = field(default_factory=ReplanHistory)
    current_node_id: Optional[str] = None

    def add_node(self, node: Node):
        self.nodes[node.id] = node
        if self.start_node_id is None:
            self.start_node_id = node.id

    def summarize_plan(self) -> str:
        summary = ""
        for n in self.nodes.values():
            summary += f"Node {n.id}: {n.task_description}, Next: {n.next_nodes}\n"
        return summary