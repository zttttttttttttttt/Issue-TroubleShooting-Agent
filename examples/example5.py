# examples/example5.py

from agent_core.agents import Agent
from agent_core.planners import GraphPlanner


def main():

    agent = Agent()
    agent.planner = GraphPlanner()

    task = "3 steps draw a digital dragon using computer emoji characters."
    agent.execute(task)

    execution_history = agent.execution_history
    print(f"Execution History: {execution_history}")
    execution_result = agent.get_execution_result_summary()
    print(f"Execution Result: {execution_result}")


if __name__ == "__main__":
    main()
