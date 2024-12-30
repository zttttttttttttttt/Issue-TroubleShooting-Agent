# agent-core - LLM Agent Framework

agent-core is a modular and extensible framework designed to facilitate the development of Language Model (LLM) agents. It provides a structured approach to defining agents, integrating various language models, and executing tasks seamlessly. Whether you’re building simple command-based agents or complex conversational agents, this framework offers the flexibility and scalability you need.

## Table of Contents

- Features
- Project Structure
- Installation
- Configuration
  - Direct Environment Variable Setting
- Usage
  - Running the Example
  - Example Script Breakdown
- Adding New Models
  - Step-by-Step Guide
  - Best Practices
- Logging
  - Logger Configuration
  - Logging Usage
- Dependencies
  - Core Dependencies
  - Additional Dependencies
  - Installation of Dependencies
- Contributing
  - Steps to Contribute
- License

## Features

- Modular Design: Separate components for agents, models, configuration, and utilities.
- Dynamic Model Loading: Automatically discover and register new models without modifying core code.
- Configuration Management: Centralized configuration handling using environment variables.
- Extensible: Easily add support for additional language models.
- Logging: Integrated logging for monitoring framework operations.

## Project Structure

 agent-core/ ├── agents/ │   ├── __init__.py │   └── agent.py ├── config/ │   ├── __init__.py │   └── config.py ├── models/ │   ├── __init__.py │   ├── base_model.py │   ├── model_registry.py │   ├── gpt_4o_mini.py │   └── gpt_35_turbo.py ├── utils/ │   ├── __init__.py │   └── logger.py ├── examples/ │   ├── __init__.py │   └── example1.py ├── requirements.txt └── README.md 

### Component Overview

- agents/: Contains the Agent class responsible for interacting with language models.
- config/: Handles configuration settings, including environment variable loading.
- models/: Houses different language model implementations and the dynamic model registry.
- utils/: Provides utility functions, including logging.
- examples/: Contains example scripts demonstrating how to use the framework.
- requirements.txt: Lists all Python dependencies required for the project.

## Installation

1. Clone the Repository

bash git clone https://github.com/lukewu8023/agent-core.git cd agent-core 

2. Create a Virtual Environment

It’s recommended to use a virtual environment to manage dependencies.

bash python -m venv .venv 

3. Activate the Virtual Environment

- Windows:

bash venv\Scripts\activate 

- Unix/Linux/MacOS:

bash source venv/bin/activate 

4. Install Dependencies

bash pip install -r requirements.txt 

## Configuration

The framework uses environment variables to manage configurations such as API keys and model settings. You can set these variables directly in your environment or use a .env file for convenience.

### Direct Environment Variable Setting

Alternatively, you can set environment variables directly in your operating system. Ensure that the following variables are set before running any scripts:

- OPENAI_API_BASE
- OPENAI_API_KEY

## Usage

### Running the Example

An example script is provided to demonstrate how to use the framework. This script initializes an agent with a specified model and executes a command.

1. Navigate to the Project Root

Ensure you’re in the root directory of the project.

bash cd agent-core

2. Run the Example Script

bash python examples/example1.py 

## Adding New Models

The framework is designed to support multiple language models. Adding a new model involves creating a new model class that inherits from BaseModel and placing it in the models/ directory.

### Step-by-Step Guide

1. Create a New Model File

For example, to add a model named NewModel, create a file new_model.py in the models/ directory.

bash touch models/new_model.py 

2. Define the Model Class

```python
# models/new_model.py

from .base_model import BaseModel
from some_language_model_library import NewModelLibrary  # Replace with actual library

class NewModel(BaseModel):
    def init(self):
        super().init(name=“new-model”)
        self.model_instance = NewModelLibrary(
            model=“new-model”,
            parameter1=value1,
            parameter2=value2,
            # Add necessary initialization parameters
        )

    def process(self, command: str) -> str:
        response = self.model_instance.execute(command)
        return response
```

Notes:

- Replace some_language_model_library and NewModelLibrary with the actual library and class names you’re using.
- Initialize the model instance with necessary parameters.

3. Automatic Registration

Once the new model file is in the models/ directory and follows the naming convention, the ModelRegistry will automatically discover and register it without any further modifications.

4. Use the New Model

Update your example script or application to use the new model.

python model = "new-model" agent = Agent(model=model) agent.execute("Your command here.") 

### Best Practices

- Consistent Naming: Use clear and consistent naming conventions for model classes and files.
- Configuration Management: If the new model requires additional configuration parameters, update the .env file accordingly.
- Error Handling: Implement robust error handling within the process method to manage potential issues during command execution.

## Logging

The framework includes an integrated logging utility to monitor operations and debug issues effectively.

### Logging Usage

Logs are automatically generated during agent initialization and command execution. You can customize the logging level and handlers as needed by modifying the Logger class.

## Dependencies

The project relies on several Python packages to function correctly. Ensure all dependencies are installed using the provided requirements.txt.

### Core Dependencies

- langchain-core==0.3.28: Core components for building language model applications.
- langchain-openai==0.2.14: OpenAI integration for LangChain.
- openai==1.58.1: OpenAI API client.
- pydantic==2.10.4: Data validation and settings management using Python type annotations.

### Additional Dependencies

- anyio==4.7.0
- certifi==2024.12.14
- charset-normalizer==3.4.1
- distro==1.9.0
- h11==0.14.0
- httpcore==1.0.7
- httpx==0.28.1
- idna==3.10
- jiter==0.8.2
- jsonpatch==1.33
- jsonpointer==3.0.0
- langsmith==0.2.6
- orjson==3.10.13
- packaging==24.2
- PyYAML==6.0.2
- regex==2024.11.6
- requests==2.32.3
- requests-toolbelt==1.0.0
- sniffio==1.3.1
- tenacity==9.0.0
- tiktoken==0.8.0
- tqdm==4.67.1
- typing_extensions==4.12.2
- urllib3==2.3.0

### Installation of Dependencies

All dependencies can be installed using pip:

bash pip install -r requirements.txt 

## Contributing

Contributions are welcome! Whether you’re fixing bugs, improving documentation, or adding new features, your input helps make this framework better.

### Steps to Contribute

1. Fork the Repository

Click the “Fork” button at the top-right corner of the repository page to create a personal copy.

2. Clone Your Fork

bash git clone https://github.com/yourusername/agent-core.git cd agent-core 

3. Create a New Branch

bash git checkout -b feature/YourFeatureName 

4. Make Changes

Implement your feature or fix.

5. Commit Your Changes

bash git add . git commit -m "Description of your changes" 

6. Push to Your Fork

bash git push origin feature/YourFeatureName 

7. Create a Pull Request

Navigate to the original repository and click “New Pull Request.” Provide a clear description of your changes.

—

Disclaimer: This framework is provided as-is without any warranties. Use it at your own risk.