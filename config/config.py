# config/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    api_base: str = os.environ.get("OPENAI_API_BASE", "")
    api_key: str = os.environ.get("OPENAI_API_KEY","")

    # Default log level (turn off informational logs by default)
    # If user sets the env var AGENT_CORE_LOG_LEVEL, we override
    _env_log_level = os.environ.get("AGENT_CORE_LOG_LEVEL", None)
    if _env_log_level:
        DEFAULT_LOG_LEVEL = _env_log_level.upper()
    else:
        DEFAULT_LOG_LEVEL = "WARNING"

    @classmethod
    def set_log_level(cls, level: str):
        """
        Update the framework-wide default log level at runtime.
        e.g., Config.set_log_level('DEBUG')
        """
        cls.DEFAULT_LOG_LEVEL = level.upper()

    DEFAULT_MODEL = "gpt-4o-mini"  # Default model name
    # You can add more configuration constants here as needed

def load_config():
    """
    Load configuration settings into environment variables.
    """
    os.environ["OPENAI_API_BASE"]=Config.api_base
    os.environ["OPENAI_API_KEY"]=Config.api_key
    # Add more environment variables or configurations here as needed
