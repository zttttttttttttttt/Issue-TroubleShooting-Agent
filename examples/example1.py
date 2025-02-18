# examples/example1.py

import sys
import os

# Add the parent directory to sys.path to allow imports from the framework
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agent_core.agents import Agent


def main():

    agent = Agent(model_name="gemini-1.5-flash-002")
    agent.execute("Who are you?")
    print(f"Response: {agent.execution_responses}")


if __name__ == "__main__":
    main()
