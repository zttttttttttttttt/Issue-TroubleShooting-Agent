# examples/example3.py

import sys
import os

# Add the parent directory to sys.path to allow imports from the framework
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agents import Agent
from planners import GenericPlanner


def main():
    agent1 = Agent()
    agent1.execute("Who are you?")

    agent2 = Agent(model="gpt-4o-mini")
    agent2.planner = GenericPlanner(model="gpt-3.5-turbo")
    task = "3 steps draw a flower"
    agent2.execute(task)


if __name__ == "__main__":
    main()
