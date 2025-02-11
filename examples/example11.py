# examples/example11.py
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agent_core.agents import Agent
from agent_core.planners.generic_planner import GenericPlanner

# Suppose you created a specialized WrittingValidator or CodingValidator
from agent_core.validators.score_validator import ScoreValidator

# from validators.coding_validator import CodingValidator
# from validators.writting_validator import WrittingValidator


def main():
    agent = Agent()
    agent.planner = GenericPlanner()

    # 1) Enable validation
    agent.enable_validators()

    # 2) See default validator mapping
    print("Default validators:", agent.validators)

    # 3) Add a new validator
    writting_validator = ScoreValidator(agent.model)
    agent.add_validator("writing", writting_validator)

    # 4) Update existing category
    coding_validator = ScoreValidator(agent.model)
    agent.update_validator("coding", coding_validator)

    print("Validators after updates:", agent.validators)

    # 5) Execute a simple task
    task = "3 steps to draw a flower"
    agent.execute(task)

    # 6) Summarize the execution
    execution_result = agent.get_execution_result_summary()
    print(f"Execution Result: {execution_result}")


if __name__ == "__main__":
    main()
