# validators/default_mapping.py

from .score_validator import ScoreValidator


def create_default_validators(model_instance):
    """
    Return a dict {category: validator_instance} tied to the given model instance.
    This is the default mapping used when an Agent is created.
    """
    return {
        "coding": ScoreValidator(model_instance),
        "summarization": ScoreValidator(model_instance),
        "action": ScoreValidator(model_instance),
        # You can add more categories here.
        # "default" can also be a fallback if desired:
        "default": ScoreValidator(model_instance),
    }
