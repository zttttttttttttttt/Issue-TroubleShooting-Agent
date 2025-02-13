# examples/example1.py

from agent_core.agents import Agent


def main():

    agent = Agent(model_name="gpt-4o-mini")
    agent.execute("Who are you?")
    print(f"Response: {agent.execution_responses}")


if __name__ == "__main__":
    main()
