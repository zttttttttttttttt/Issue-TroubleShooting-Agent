# examples/example5.py

import sys
import os

# Add the parent directory to sys.path to allow imports from the framework
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from agent_core.agents import Agent
from agent_core.planners import GraphPlanner


def main():

    agent = Agent()
    agent.planner = GraphPlanner(model_name="gemini-1.5-pro-002")
    agent.enable_evaluators()

    task = "3 steps draw a digital dragon using computer emoji characters."
    agent.execute(task)

    execution_history = agent.execution_history
    print(f"Execution History: {execution_history}")
    execution_result = agent.get_execution_result_summary()
    print(f"Execution Result: {execution_result}")


if __name__ == "__main__":
    main()
