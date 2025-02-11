# agents/agent.py
import os
from typing import Optional, List

from agent_core.planners.generic_planner import GenericPlanner
from agent_core.planners.graph_planner import GraphPlanner
from agent_core.validators.validators import get_validators
from agent_core.validators.base_validator import BaseValidator
from agent_core.models.model_registry import ModelRegistry
from agent_core.utils.logger import get_logger
from agent_core.utils.context_manager import get_context
from agent_core.utils.llm_chat import LLMChat


class Agent:
    """
    The Agent coordinates task execution with or without a Planner.
    It now exposes two prompts:
      - execute_prompt: overrides how we generate the no-planner prompt
      - summary_prompt (used in get_execution_result)
    """

    DEFAULT_EXECUTE_PROMPT = """\
{context_section}
{background}
<Task> 
{task}
</Task>
"""

    DEFAULT_SUMMARY_PROMPT = """\
You are an assistant summarizing the outcome of a multi-step plan execution.
Below is the complete step-by-step execution history. Provide a concise,
well-structured summary describing how the solution was achieved and any
notable details. Include each step's role in the final outcome.

Execution History:
{history_text}

Summary:
"""

    def __init__(self, model: Optional[str] = None, log_level: Optional[str] = None):
        """
        If 'model' is not provided, the default model from config will be used.
        'log_level' can override the framework-wide default for this Agent specifically.
        """
        self.logger = get_logger("agent", log_level)
        self._model = None
        self._planner = None
        self.tools = None
        # This list holds execution data for each step in sequence.
        # Example entry:
        # {
        #   "step_name": "Draw the stem",
        #   "step_description": "Draw a vertical line as the flower's stem",
        #   "step_result": "Stem drawn successfully."
        # }
        self._execution_history = []

        # Default knowledge / background
        self.knowledge = ""  # Used to guide how we make plans
        self.background = ""  # Used during execution steps

        # The context manager (use get_context())
        self._context = get_context()

        # Prompt strings for direct (no-planner) usage and summary
        self._execute_prompt = self.DEFAULT_EXECUTE_PROMPT
        self._summary_prompt = self.DEFAULT_SUMMARY_PROMPT

        if not model:
            model = os.getenv("DEFAULT_MODEL")

        # Use the property setter to initialize the model
        self.model = model

        # NEW: Validator management
        self.validators_enabled = False
        self._validators = {}
        self._load_default_validators()

        # Provide an LLM tool instance so user can do `agent.llm_chat.process(...)`
        self.llm_chat = LLMChat(self._model.name, log_level)
        self.logger.info("Agent instance created with a LLM chat tool.")

        self.logger.info("Agent instance created.")

    @property
    def context(self):
        """
        Expose the agent's context manager so we can do:
          c = agent.context
          c.add_context("role", "...")
        """
        return self._context

    @property
    def execute_prompt(self) -> str:
        """Prompt used when no planner is set (single-step)."""
        return self._execute_prompt

    @execute_prompt.setter
    def execute_prompt(self, value: str):
        self._execute_prompt = value

    @property
    def summary_prompt(self) -> str:
        """Prompt used for final summarizing of execution history."""
        return self._summary_prompt

    @summary_prompt.setter
    def summary_prompt(self, value: str):
        self._summary_prompt = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model_name: str):
        model = ModelRegistry.get_model(model_name)
        if not model:
            self.logger.error(f"Model '{model_name}' not found in registry.")
            raise ValueError(f"Model '{model_name}' is not supported.")
        self._model = model
        self.logger.info(f"Agent model set to: {model.name}")

    @property
    def planner(self):
        return self._planner

    @planner.setter
    def planner(self, planner):
        # We still allow either GenericPlanner or GraphPlanner, but now both inherit from BasePlanner.
        if not isinstance(planner, (GenericPlanner, GraphPlanner)):
            self.logger.error(
                "Planner must be an instance of GenericPlanner or GraphPlanner."
            )
            raise TypeError(
                "Planner must be an instance of GenericPlanner or GraphPlanner."
            )
        self._planner = planner
        self.logger.info(f"Agent planner set to: {planner.__class__.__name__}")

    @property
    def execution_history(self) -> List[dict]:
        """
        Read-only access to the execution history.
        Each item is a dict with keys: 'step_name', 'step_description', 'step_result'.
        """
        return self._execution_history

    @property
    def execution_responses(self) -> str:
        """
        Read-only access to the execution responses.
        Combine all 'step_result' together.
        """
        responses_text = execution_history_to_responses(self._execution_history)
        return responses_text

    def _load_default_validators(self):
        """
        Load a default mapping of category -> validator (all referencing the current model).
        Make a local copy so user modifications won't affect the original file.
        """
        validators = get_validators(self._model)
        self._validators = dict(validators)

    @property
    def validators(self):
        """
        Return the current validator mapping (category -> validator).
        """
        return self._validators

    def add_validator(self, category: str, validator: BaseValidator):
        """
        Insert or override a validator for the given category.
        """
        self._validators[category] = validator

    def update_validator(self, category: str, validator: BaseValidator):
        """
        Update the validator for an existing category.
        If the category doesn't exist, we log a warning and add it.
        """
        if category in self._validators:
            self._validators[category] = validator
        else:
            self.logger.warning(
                f"Category '{category}' not found in validators. Creating new entry."
            )
            self._validators[category] = validator

    def enable_validators(self):
        self.validators_enabled = True
        self.logger.info("Validators have been enabled.")

    def disable_validators(self):
        self.validators_enabled = False
        self.logger.info("Validators have been disabled.")

    def execute(self, task: str):
        """
        1) If no planner, do direct single-step with the model (use background).
        2) If planner, plan(...) -> then call execute_plan(...).
        """
        self.logger.info(f"Agent is executing task: {task}")

        # Case 1: No planner => direct single-step
        if not self._planner:
            # Possibly build a context_section from the context
            context_section = self._context.context_to_str()
            final_prompt = self._execute_prompt.format(
                context_section=context_section,
                background=background_format(self.background),
                task=task,
            )
            response = self._model.process(final_prompt)
            self.logger.info(f"Response: {response}")
            self._execution_history.append(
                {
                    "step_name": "Direct Task Execution",
                    "step_description": task,
                    "step_result": str(response),
                }
            )
            return response

        # Case 2: Using a planner => first create steps/graph
        current_categories = list(self._validators.keys())
        steps = self._planner.plan(
            task,
            self.tools,
            execute_history=self._execution_history,
            knowledge=self.knowledge,
            background=background_format(self.background),
            categories=current_categories,
            agent=self,
        )

        # Now just call planner's execute_plan(...) in a unified way
        return self._planner.execute_plan(
            steps=steps,
            execution_history=self._execution_history,
            agent=self,
            context_manager=self._context,
            background=self.background,
        )

    def get_execution_result_summary(self) -> str:
        """
        Produce an overall summary describing how the solution was completed,
        using the LLM (agent's model) to format the final explanation if desired.
        """
        if not self._execution_history:
            return (
                "No direct step-based execution history recorded. "
                "(If you used GraphPlanner, the node-based execution is stored inside the planner.)"
            )

        history_text = execution_history_to_str(self._execution_history)
        final_prompt = self._summary_prompt.format(history_text=history_text)

        self.logger.info("Generating final execution result (summary).")
        summary_response = self._model.process(final_prompt)
        return str(summary_response)


# Build a textual representation of the execution history
def execution_history_to_str(execution_history: list):
    history_lines = []
    for idx, record in enumerate(execution_history, 1):
        line = (
            f"Step {idx}: {record['step_name']}\n"
            f"Description: {record['step_description']}\n"
            f"Result: {record['step_result']}\n"
        )
        history_lines.append(line)

    history_text = "\n".join(history_lines)
    return history_text


def execution_history_to_responses(execution_history: list):
    response_lines = []
    for idx, record in enumerate(execution_history, 1):
        line = f"{record['step_result']}\n"
        response_lines.append(line)

    responses_text = "".join(response_lines)
    if responses_text.endswith("\n"):
        responses_text = responses_text[:-1]

    return responses_text


def background_format(background: str):
    background_str = ""
    if background != "":
        background_str = "<Background>\n"
        background_str += f"{background}\n"
        background_str += "</Background>\n"
    return background_str
