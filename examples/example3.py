# examples/example3.py

from agent_core.agents import Agent
from agent_core.planners import GenericPlanner


def main():
    agent1 = Agent()
    agent1.execute("Who are you?")

    agent2 = Agent(model_name="gpt-4o-mini")
    agent2.planner = GenericPlanner(model_name="gpt-3.5-turbo")
    task = "3 steps draw a flower"
    agent2.execute(task)


if __name__ == "__main__":
    main()
