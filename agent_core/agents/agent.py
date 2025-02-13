import os
from typing import Optional, List

from langchain_core.tools import BaseTool

from agent_core.entities.steps import Steps, Step
from agent_core.models.base_model import BaseModel
from agent_core.planners.base_planner import BasePlanner
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

    DEFAULT_EXECUTE_PROMPT = """
{context_section}
{background}
<Task> 
{task}
</Task>
"""

    DEFAULT_SUMMARY_PROMPT = """
You are an assistant summarizing the outcome of a multi-step plan execution.
Below is the complete step-by-step execution history. Provide a concise,
well-structured summary describing how the solution was achieved and any
notable details. Include each step's role in the final outcome.

Execution History:
{history_text}

Summary:
"""

    def __init__(self, model_name: Optional[str] = None,
                 log_level: Optional[str] = None):
        """
        If 'model' is not provided, the default model from config will be used.
        'log_level' can override the framework-wide default for this Agent specifically.
        """

        # This list holds execution data for each step in sequence.
        self._execution_history: Steps = Steps()
        self._model: Optional[BaseModel] = None
        self._model_name: Optional[str] = None

        self.logger = get_logger("agent", log_level)
        self.planner = None
        self.tools: Optional[List[BaseTool]] = None

        # Default knowledge / background
        self.knowledge = ""  # Used to guide how we make plans
        self.background = ""  # Used during execution steps

        # The context manager (use get_context())
        self.context = get_context()

        # Prompt strings for direct (no-planner) usage and summary
        self.execute_prompt = self.DEFAULT_EXECUTE_PROMPT
        self.summary_prompt = self.DEFAULT_SUMMARY_PROMPT

        # Use the property setter to initialize the model
        self.model_name = model_name if model_name else os.getenv("DEFAULT_MODEL")

        # NEW: Validator management
        self.validators_enabled = False
        self.validators = {}
        self._load_default_validators()

        # Provide an LLM tool instance so user can do `agent.llm_chat.process(...)`
        self.llm_chat = LLMChat(self.model_name, log_level)
        self.logger.info("Agent instance created.")

    def execute(self, task: str):
        """
        1) If no planner, do direct single-step with the model (use background).
        2) If planner, plan(...) -> then call execute_plan(...).
        """
        self.logger.info(f"Agent is executing task: {task}")

        # Case 1: No planner => direct single-step
        if not self.planner:
            # Possibly build a context_section from the context
            context_section = self.context.context_to_str()
            final_prompt = self.execute_prompt.format(
                context_section=context_section,
                background=background_format(self.background),
                task=task,
            )
            response = self._model.process(final_prompt)
            self.logger.info(f"Response: {response}")
            self._execution_history.add_step(
                Step(
                    name="Direct Task Execution",
                    description=task,
                    result=str(response)
                )
            )
            return response

        # Case 2: Using a planner => first create steps/graph
        current_categories = list(self.validators.keys())
        plan = self.planner.plan(
            task,
            self.tools,
            execute_history=self._execution_history,
            knowledge=self.knowledge,
            background=background_format(self.background),
            categories=current_categories,
        )

        # Now just call planner's execute_plan(...) in a unified way
        return self.planner.execute_plan(
            plan=plan,
            execution_history=self._execution_history,
            context_manager=self.context,
            background=self.background,
            validators_enabled=self.validators_enabled,
            validators=self.validators,
            llm_chat=self.llm_chat
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

        history_text = self._execution_history.execution_history_to_str()
        final_prompt = self.summary_prompt.format(history_text=history_text)

        self.logger.info("Generating final execution result (summary).")
        summary_response = self._model.process(final_prompt)
        return str(summary_response)

    def planner(self, planner):
        if not issubclass(planner.__class__, BasePlanner):
            error_msg = "Planner must be an instance of BasePlanner."
            self.logger.error(error_msg)
            raise TypeError(error_msg)
        self.planner = planner
        self.logger.info(f"Agent planner set to: {planner.__class__.__name__}")

    @property
    def model_name(self):
        return self._model_name

    @model_name.setter
    def model_name(self, model_name: str):
        self._model_name = model_name
        self._model = ModelRegistry.get_model(model_name)
        self.logger.info(f"Agent model set to: {model_name}")

    @property
    def execution_history(self) -> Steps:
        """
        Read-only access to the execution history.
        Each item is a dict with keys: 'step_name', 'step_description', 'step_result'.
        """
        return self._execution_history

    @execution_history.setter
    def execution_history(self, value):
        raise AttributeError("Cannot modify read-only attribute.")

    def enable_validators(self):
        self.validators_enabled = True
        self.logger.info("Validators have been enabled.")

    def disable_validators(self):
        self.validators_enabled = False
        self.logger.info("Validators have been disabled.")

    @property
    def execution_responses(self) -> str:
        """
        Read-only access to the execution responses.
        Combine all 'step_result' together.
        """
        return self._execution_history.execution_history_to_responses()

    def _load_default_validators(self):
        """
        Load a default mapping of category -> validator (all referencing the current model).
        Make a local copy so user modifications won't affect the original file.
        """
        validators = get_validators(self._model)
        self.validators = dict(validators)

    def add_validator(self, category: str, validator: BaseValidator):
        """
        Insert or override a validator for the given category.
        """
        self.validators[category] = validator

    def update_validator(self, category: str, validator: BaseValidator):
        """
        Update the validator for an existing category.
        If the category doesn't exist, we log a warning and add it.
        """
        if category in self.validators.keys():
            self.validators[category] = validator
        else:
            self.logger.warning(
                f"Category '{category}' not found in validators. Creating new entry."
            )
            self.validators[category] = validator


def background_format(background: str):
    background_str = ""
    if background != "":
        background_str = f"<Background>\n{background}\n</Background>\n"
    return background_str
