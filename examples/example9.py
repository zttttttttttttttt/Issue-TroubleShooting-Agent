# examples/example9.py

import sys
import os

# Add the parent directory to sys.path to allow imports from the framework
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agents import Agent
from planners import GenericPlanner
from validators.score_validator import ScoreValidator

from config.config import Config

# Globally sets the log level to DEBUG for detailed logging across the framework
Config.set_log_level("DEBUG")


def main():
    """
    Demonstrates how to override default prompts for:
    1) Validator (ScoreValidator)
    2) Agent single-step execution
    3) Planner multi-step prompt
    4) Agent's final summary prompt

    These overrides only apply to the current instances of validator, agent, and planner.
    Once a new object is created, it will revert to the default prompt.
    """

    # --- 1) OVERRIDE ScoreValidator Prompt ----------------------------------
    validator = ScoreValidator()
    # Print current default validator prompt
    print("Default Validator Prompt:\n", validator.prompt)

    # Replace it with a grammar-focused prompt; note the placeholders {request} and {response} must remain
    validator.prompt = """\
    You are a special validator focusing on only grammar correctness.
    Subtask: {request}
    Output: {response}
    Please check grammar only.
    """

    # --- 2) OVERRIDE Agent Execution Prompt ---------------------------------
    agent = Agent()

    # Print the Agent's default single-step execution prompt
    print("Default Agent Execution Prompt:\n", agent.execute_prompt)

    # Override the agent's single-step prompt
    # Valid placeholders here are {task} and {background} (and {context_section} if you need it).
    agent.execute_prompt = (
        "Customized single-step prompt.\n" "Task: {task}\n" "Background: {background}\n"
    )

    # Provide some background context for the agent (this is optional, but demonstrates usage)
    agent.background = "I am a helpful assistant."

    # --- 3) OVERRIDE GenericPlanner Prompt -----------------------------------
    planner = GenericPlanner()

    # Print the default planner prompt
    print("Default Planner Prompt:\n", planner.prompt)

    # Override the planner's prompt to produce exactly two steps in JSON
    # Placeholders typically include: {task}, {tools_knowledge}, {knowledge}, {example_json1}, {example_json2}.
    planner.prompt = """\
    I only want two simple steps:
    Task: {task}
    Tools: {tools_knowledge}
    Output JSON with two main steps.
    Present each step in JSON format with the attributes 'step_name', 'step_description', 'use_tool', and optionally 'tool_name', and 'step_category'.
    """

    # Attach this planner to the agent
    agent.planner = planner

    # Now execute a simple task that will be broken into steps by the new planner prompt
    result = agent.execute("draw a flower")
    print("Execution result:", result)

    # --- 4) OVERRIDE Agent Summary Prompt ------------------------------------
    # Print the current default summary prompt
    print("Default Agent Summary Prompt:\n", agent.summary_prompt)

    # Replace it with a custom summary format
    # The placeholder {history_text} is used to inject the step-by-step details.
    agent.summary_prompt = "Here is a custom summary for steps:\n{history_text}"

    # Retrieve and print the final execution summary
    print(agent.get_execution_result_summary())


if __name__ == "__main__":
    main()
