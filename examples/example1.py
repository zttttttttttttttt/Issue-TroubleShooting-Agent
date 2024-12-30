import sys
import os

# Add the parent directory to sys.path to allow imports from the framework
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agents import Agent


def main():
    model = "gpt-4o-mini"

    agent = Agent(model=model)
    agent.execute("Who are you?")


if __name__ == "__main__":
    main()
