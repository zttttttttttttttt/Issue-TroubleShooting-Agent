import sys
import os

# Add the parent directory to sys.path to allow imports from the framework
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agents import Agent
from planners import GenericPlanner


def main():

    agent = Agent()
    agent.model = "gpt-4o-mini"
    agent.planner = GenericPlanner()

    task = "Build a react web applicaiton, click button will popup hello world on the screen."
    agent.execute(task)


if __name__ == "__main__":
    main()
