# models/model_registry.py

import pkgutil
import importlib
import os

from .base_model import BaseModel  # Updated import
from agent_core.utils.logger import get_logger


def load_models_dynamically(logger):    
    """
    Dynamically load and register all model classes from the models package.
    """
    package_dir = os.path.dirname(__file__)
    package_name = __package__  # Should be 'models'

    for _, module_name, _ in pkgutil.iter_modules([package_dir]):
        if module_name.startswith("_") or module_name in ["model_registry", "base_model"]:
            continue  # Skip private modules and model_registry itself
        module = importlib.import_module(f".{module_name}", package=package_name)
        # Iterate through attributes to find subclasses of BaseModel
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if (
                isinstance(attribute, type)
                and issubclass(attribute, BaseModel)
                and attribute is not BaseModel
            ):
                instance = attribute()
                ModelRegistry.register_model(instance)


class ModelRegistry:
    _models = {}
    logger = get_logger("model-registry")

    @classmethod
    def register_model(cls, model: BaseModel):
        cls._models[model.name] = model
        cls.logger.info(f"Registered model: {model.name}")

    @classmethod
    def get_model(cls, name: str):
        return cls._models.get(name, None)

    @classmethod
    def load_models(cls, log_level: str = None):
        logger = get_logger("model-loader", log_level)
        try:
            load_models_dynamically(logger)
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise


# Initialize and load models
ModelRegistry.load_models()
