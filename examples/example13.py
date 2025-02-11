# examples/example13.py
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agents.agent import Agent
from planners.generic_planner import GenericPlanner

from validators.coding_validator import CodingValidator

def main():
    agent = Agent()
    agent.planner = GenericPlanner()

    # 1) Enable validation
    agent.enable_validators()

    # 2) See default validator mapping
    print("Default validators:", agent.validators)

    # 3) Add a new validator
    coding_validator = CodingValidator(agent.model)
    agent.add_validator("coding", coding_validator)

    print("Validators after updates:", agent.validators)

    # 4) Execute a simple task
    task = "Implement a function that calculates the factorial of a number, with proper error handling and documentation."
    agent.execute(task)

    # 5) Summarize the execution
    execution_result = agent.get_execution_result_summary()
    print(f"Execution Result: {execution_result}")


if __name__ == "__main__":
    main()
