# utils/llm_chat.py

import re
from models.model_registry import ModelRegistry
from config.config import Config
from utils.logger import get_logger


class LLMChat:

    DEFAULT_EVALUATE_TEXT_PROMPT = """\
You are a critical evaluator. Below is some text to evaluate:

Text:
{input_text}

Criteria:
{criteria}

Instructions:
1) Provide a short explanation of how well the text meets the criteria.
2) Then on a new line, output "Rating: X" where X is an integer in [1..10].
3) Optionally provide suggestions.

Example:
Summary: This text partially meets the criteria but could be more clear.
Rating: 7
Suggestions: Make it clearer how the data is processed.

Now, produce your evaluation:
"""

    def __init__(self, model_name: str = None, log_level: str = None):
        """
        If model_name is None, use the default model from Config.
        This class can be used to do both summarization and text-critique.
        """
        self.logger = get_logger("llm_chat", log_level)
        if not model_name:
            model_name = Config.DEFAULT_MODEL

        self.model_name = model_name
        self.model = ModelRegistry.get_model(self.model_name)
        if not self.model:
            raise ValueError(f"Model '{self.model_name}' not found in registry.")
        self.logger.info(f"LLMChat initialized with model: {self.model.name}")

        self._evaluate_text_prompt = self.DEFAULT_EVALUATE_TEXT_PROMPT

    @property
    def evaluate_text_prompt(self) -> str:
        """Prompt used for evaluating text."""
        return self._evaluate_text_prompt

    @evaluate_text_prompt.setter
    def evaluate_text_prompt(self, value: str):
        self._evaluate_text_prompt = value

    def process(self, request: str) -> str:
        response = self.model.process(request)
        self.logger.debug(f"Response: {response}")
        return response.strip()

    def evaluate_text(
        self, input_text: str, criteria: str = "", rating_threshold: int = 8
    ) -> dict:
        """
        Critique/evaluate the text using the DEFAULT_EVALUATE_TEXT_PROMPT.
        Returns a dict with keys:
          - 'decision': "Pass" or "Fail" based on rating_threshold
          - 'rating': the integer rating from 1..10
          - 'summary': the extracted text around "Summary:"
          - 'suggestions': text after "Suggestions:" if found
          - 'raw_response': the entire LLM response

        Example usage:
            result = llm.critic_text("some plan", "Should talk about DB usage", 8)
            if result["decision"] == "Fail":
                # handle test fail logic
        """
        prompt = self.DEFAULT_EVALUATE_TEXT_PROMPT.format(
            input_text=input_text,
            criteria=criteria,
        )
        response = self.model.process(prompt)
        self.logger.debug(f"Evaluate raw response: {response}")

        # Parse rating from 1..10
        rating_val = self._parse_rating(response)
        decision = "Pass" if rating_val >= rating_threshold else "Fail"

        # Optionally parse 'Summary:' and 'Suggestions:'
        summary_str = self._parse_section(response, "summary")
        suggestions_str = self._parse_section(response, "suggestions")

        return {
            "decision": decision,
            "rating": rating_val,
            "summary": summary_str,
            "suggestions": suggestions_str,
            "raw_response": response,
        }

    def _parse_rating(self, response_text: str) -> int:
        """
        Find 'Rating: X' in the text. Return X as an integer. Default to 1 if not found.
        """
        match = re.search(r"Rating:\s*(\d+)", response_text, re.IGNORECASE)
        if match:
            return min(10, max(1, int(match.group(1))))  # clamp rating to [1..10]
        return 1

    def _parse_section(self, response_text: str, label: str) -> str:
        """
        Extract text after the given label, e.g. "Summary:" or "Suggestions:".
        Returns the found text or a default string.
        Example: label="summary" => look for "Summary:"
        """
        pattern = rf"{label}:\s*(.*)"
        match = re.search(pattern, response_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return f"No {label} found."
