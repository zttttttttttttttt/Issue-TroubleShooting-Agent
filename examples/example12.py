# examples/example12.py

from agent_core.agents import Agent
from agent_core.planners.generic_planner import GenericPlanner


def main():
    agent = Agent()
    agent.planner = GenericPlanner()

    print(agent.llm_chat.evaluate_text_prompt)
    print(agent.llm_chat.process("Who are you?"))

    task = "3 steps to write a poem about flower"
    agent.execute(task)

    execution_history = agent.execution_history
    print(f"Execution History: {execution_history}")
    execution_result = agent.llm_chat.process(
        f"Summarize the execution history: {execution_history}"
    )
    print(f"Execution Result: {execution_result}")


if __name__ == "__main__":
    main()
