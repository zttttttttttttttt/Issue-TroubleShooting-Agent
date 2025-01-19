# examples/example9.py

import sys
import os

# Add the parent directory to sys.path to allow imports from the framework
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agents import Agent
from planners import GenericPlanner


def main():

    # 1) Overriding the ScoreValidator prompt
    # validator = ScoreValidator(model=..., log_level="DEBUG")
    # print("Default Validator Prompt:\n", validator.prompt)

    # validator.prompt = """\
    # You are a special validator focusing on only grammar correctness.
    # Subtask: {request}
    # Output: {response}
    # Please check grammar only.
    # """

    # 2) Overriding the Agent's direct execution prompt
    # agent = Agent()
    # agent.direct_prompt = "Customized single-step prompt.\nTask: {task}\nBackground: {background}\n"
    # agent.background = "I am a helpful assistant."

    # result = agent.execute("Say hi to me.")
    # print("Execution result:", result)

    # 3) Overriding the final summary prompt
    # agent.summary_prompt = "Here is a custom summary for steps:\n{history_text}"
    # print(agent.get_execution_result())

    # 4) Overriding the GenericPlanner prompt
    # planner = GenericPlanner()
    # planner.plan_prompt = """\
    # I only want a single step:
    # Task: {task}
    # Tools: {tools_knowledge}
    # Output JSON with one step.
    # """
    # agent.planner = planner

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
