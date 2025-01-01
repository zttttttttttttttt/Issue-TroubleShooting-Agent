import os


class Config:
    DEFAULT_MODEL = "gpt-4o-mini"  # Default model name
    # You can add more configuration constants here as needed


def load_config():
    """
    Load configuration settings into environment variables.
    """
    os.environ["OPENAI_API_BASE"] = "https://api.ohmygpt.com/v1/"
    os.environ["OPENAI_API_KEY"] = ""
    # Add more environment variables or configurations here as needed
