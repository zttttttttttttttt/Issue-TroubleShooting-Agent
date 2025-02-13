from typing import List, Optional


class Step:

    def __init__(self, name: str, description: str,
                 result: Optional[str] = None,
                 use_tool: Optional[bool] = None,
                 tool_name: Optional[str] = None,
                 category: Optional[str] = "default"):
        self.name = name
        self.description = description
        self.result = result
        self.use_tool = use_tool
        self.tool_name = tool_name
        self.category = category

    def __repr__(self):
        return (
            f"Step(name='{self.name}', description='{self.description}', "
            f"use_tool='{self.use_tool}', tool_name='{self.tool_name}', category='{self.category}')"
        )

    def to_dict(self):
        # Convert the object to a dictionary that can be serialized to JSON
        return {
            "name": self.name,
            "description": self.description,
            "use_tool": self.use_tool,
            "tool_name": self.tool_name,
            "category": self.category,
        }


class Steps:

    steps: List[Step] = []

    def __str__(self):
        return self.execution_history_to_str()

    # Build a textual representation of the execution history
    def execution_history_to_str(self):
        history_lines = []
        for idx, step in enumerate(self.steps, 1):
            line = (
                f"Step {idx}: {step.name}\n"
                f"Description: {step.description}\n"
                f"Result: {step.result}\n"
            )
            history_lines.append(line)
        history_text = "\n".join(history_lines)
        return history_text

    def execution_history_to_responses(self):
        response_lines = []
        for step in self.steps:
            line = f"{step.result}\n"
            response_lines.append(line)

        responses_text = "".join(response_lines)
        if responses_text.endswith("\n"):
            responses_text = responses_text[:-1]

        return responses_text

    def add_step(self, step: Step):
        self.steps.append(step)
