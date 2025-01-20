# validators/base_validator.py

from abc import ABC, abstractmethod


class BaseValidator(ABC):
    """
    A base class for all validators. Every validator must implement `validate()`.
    """

    @abstractmethod
    def validate(self, request: str, response: str):
        """
        Perform validation on the given request and response.
        Must return a tuple: (decision, score, details).

        - decision (str): "Accept Output" or "Rerun Subtask"
        - score (int or float): a numeric measure of quality
        - details (dict): optional extra data, e.g., breakdown of scores
        """
        pass
