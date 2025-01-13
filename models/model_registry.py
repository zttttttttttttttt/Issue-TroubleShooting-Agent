# models/model_registry.py

from abc import ABC, abstractmethod
import pkgutil
import importlib
import os
import logging

from config.config import load_config
from .base_model import BaseModel  # Updated import


def load_models_dynamically():
    """
    Dynamically load and register all model classes from the models package.
    """
    package_dir = os.path.dirname(__file__)
    package_name = __package__  # Should be 'models'

    for _, module_name, _ in pkgutil.iter_modules([package_dir]):
        if module_name.startswith("_") or module_name == "model_registry":
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
    logger = logging.getLogger("LLMAgentFramework")

    @classmethod
    def register_model(cls, model: BaseModel):
        cls._models[model.name] = model
        cls.logger.info(f"Registered model: {model.name}")

    @classmethod
    def get_model(cls, name: str) -> BaseModel:
        return cls._models.get(name, None)

    @classmethod
    def load_models(cls):
        load_config()  # Ensure configuration is loaded first
        try:
            load_models_dynamically()
        except Exception as e:
            cls.logger.error(f"Error loading models: {e}")
            raise


# Initialize and load models
ModelRegistry.load_models()
