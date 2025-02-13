# examples/example7.py

from agent_core.agents import Agent
from agent_core.planners import GenericPlanner


def main():

    agent = Agent("gpt-4o-mini")
    agent.planner = GenericPlanner(model_name="gpt-3.5-turbo")

    agent.knowledge = "to draw a object you need to take 3 steps, 1) prepare tools, 2) prepare paper, 3) draw the object"
    agent.background = "You are a professional artist"

    task = "draw a flower"
    agent.execute(task)


if __name__ == "__main__":
    main()
