# examples/example4.py

import sys
import os

# Add the parent directory to sys.path to allow imports from the framework
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agents import Agent
from planners import GenericPlanner


def main():

    agent = Agent(model="gpt-4o-mini")

    planner = GenericPlanner(model="gpt-3.5-turbo")
    print(planner.prompt)

    planner.prompt = """\
    I only want a single step:
    Task: {task}
    Tools: {tools_knowledge}
    Output JSON with one step.
    """
    agent.planner = planner

    task = "3 steps draw a flower"
    agent.execute(task)

    execution_history = agent.execution_history
    print(execution_history)
    execution_result = agent.get_execution_result()
    print(execution_result)


if __name__ == "__main__":
    main()
