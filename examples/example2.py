# examples/example2.py

from agent_core.agents import Agent
from agent_core.planners import GenericPlanner


def main():

    agent = Agent("gpt-4o-mini")
    agent.planner = GenericPlanner()

    task = "3 steps draw a flower."
    agent.execute(task)


if __name__ == "__main__":
    main()
