# examples/example11.py

from agent_core.agents import Agent
from agent_core.planners.generic_planner import GenericPlanner
from agent_core.validators.score_validator import ScoreValidator


def main():
    agent = Agent()
    agent.planner = GenericPlanner()

    # 1) Enable validation
    agent.enable_validators()

    # 2) See default validator mapping
    print("Default validators:", agent.validators)

    # 3) Add a new validator
    writing_validator = ScoreValidator(agent.model_name)
    agent.add_validator("writing", writing_validator)

    # 4) Update existing category
    coding_validator = ScoreValidator(agent.model_name)
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
