# [agent-core] LLM Agent Framework

A comprehensive, example-driven framework for orchestrating tasks using Large Language Models (LLMs). This project demonstrates how to build agents that plan and execute tasks in both a **step-by-step** manner (via a `GenericPlanner`) or via a **graph-based** approach (via a `GraphPlanner`). The framework provides:

- **Agent** classes that can be configured with different planners and models.
- **Planner** classes to break down tasks step-by-step or build a node-based plan graph.
- **Model** classes that dynamically load and interact with various LLM backends.
- **Validator** classes that evaluate the correctness of each step or node output.

This repository includes multiple **examples** showcasing different use-cases.

---

## Table of Contents

1. [Project Introduction](#project-introduction)
2. [Features](#features)
3. [File Structure](#file-structure)
4. [Installation](#installation)
5. [Dynamic Model Creation](#dynamic-model-creation)
6. [Usage](#usage)
7. [Contributing](#contributing)
8. [License](#license)

---

## Project Introduction

This LLM Agent Framework aims to streamline task execution and planning workflows through:

- **Agent** objects that receive high-level tasks.
- **Planners** that decompose these tasks into multiple steps (or nodes) automatically using a Large Language Model.
- **Execution** of each step or node, capturing intermediate outputs and verifying correctness via an LLM-based score validator.
- **Adaptive** re-planning when steps fail to meet a validation threshold.

From straightforward tasks (“Who are you?”) to multi-step workflows (“draw a flower in multiple steps”), the framework abstracts away the complexities of LLM usage, while providing extensibility to integrate additional models or custom logic.

---

## Features

1. **Multiple Models**: Easily switch between different OpenAI-based or custom LLMs by registering them in `ModelRegistry`.
2. **Two Planner Strategies**:
   - **GenericPlanner**: Generates a simple list of steps (JSON-based) and executes them one by one.
   - **GraphPlanner**: Builds a directed graph of nodes, executes them in sequence, and can re-plan on failure.
3. **Step-by-step Validation**: Each step (or node) is evaluated by a `ScoreValidator` that uses LLM-based scoring logic.
4. **Dynamic Model Loading**: Place a new model in `models/` and it is automatically picked up and registered.
5. **Example-Driven**: Multiple examples (`examples/`) demonstrate usage from simple to more complex scenarios.

---

## File Structure

.
├── agents/
│ └── agent.py # Main Agent class
├── planners/
│ ├── generic_planner.py # Step-based plan generation & execution
│ └── graph_planner.py # Graph-based planning and execution logic
├── models/
│ ├── base_model.py # Abstract BaseModel class
│ ├── gpt_4o_mini.py # Example GPT-4o-mini model
│ ├── gpt_35_turbo.py # Example GPT-3.5-turbo model
│ └── model_registry.py # Dynamic model registry & loader
├── validators/
│ └── score_validator.py # Score-based LLM validator
├── utils/
│ ├── context_manager.py # Maintains context during node-based execution
│ └── logger.py # Custom logger
├── config/
│ ├── config.py # Holds default config, e.g., default model
│ └── init.py
├── examples/
│ ├── example1.py # Simple usage (Agent with direct execution)
│ ├── example2.py # Agent + GenericPlanner usage
│ ├── example3.py # Multiple agents & planners
│ ├── example4.py # Accessing agent execution history
│ └── example5.py # GraphPlanner demonstration
└── README.md # Project readme (this file)

---

## Installation

#### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/agent-core.git
cd llm-agent-framework
```

#### 2. (Optional) Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### 3. Install the project as a library

If there is a setup.py file in the root directory, you can do:

```bash
pip install -e .
```

If no setup.py is present, you can install by referencing the directory:

```bash
pip install -e path/to/agent-core
```

This will make the agents, planners, models, etc. available in your Python environment.

## Dynamic Model Creation

To add or modify models that the framework can use:

#### 1. Create a new file in models/, e.g., my_new_model.py.

#### 2. Extend the BaseModel class. For example:

```python
from .base_model import BaseModel

class MyNewModel(BaseModel):
    def __init__(self):
        super().__init__(name="my-new-model")
        # Initialize your model connection / client here

    def process(self, request: str) -> str:
        # Call your model's API or logic, then return the string result
        response = ...
        return response
```

#### 3. Register automatically: The model_registry.py uses dynamic loading to discover new subclasses of BaseModel. Once your file is in models/, it will be registered at runtime.

#### 4. Use your new model:

```python
from agents import Agent

agent = Agent(model="my-new-model")
response = agent.execute("Hello, new model!")
```

No additional configuration needed—just ensure your model’s class is named properly and placed in the models/ directory.

## Usage

We provide multiple examples in the examples/ folder to illustrate various ways of using the framework:

#### 1. Example 1: example1.py

Demonstrates a basic Agent using direct execution (no planner).

```bash
python examples/example1.py
```

#### 2. Example 2: example2.py

Shows how to attach a GenericPlanner to the agent to generate steps.

```bash
python examples/example2.py
```

#### 3. Example 3: example3.py

Illustrates using multiple agents (with different models) and planners.

#### 4. Example 4: example4.py

Demonstrates retrieving the agent’s execution_history and final execution_result.

#### 5. Example 5: example5.py

Uses the GraphPlanner for node-based planning, demonstrating validation & re-planning.

#### General Workflow:

1. Instantiate an Agent with a chosen model (or use the default).
2. Optionally set a planner:

- GenericPlanner (step-based).
- GraphPlanner (node-based).

3. Call agent.execute("Your task").
4. For step-based planners, each step is automatically executed and recorded.
5. For graph-based planners, the plan (nodes) is built and executed with possible re-planning on failure.
6. Access agent.execution_history or call agent.get_execution_result() for a final summary.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear messages.
4. Push your branch to your fork.
5. Submit a Pull Request (PR) to the main repository.

Guidelines

- Write clear commit messages.
- Ensure your changes are tested (new or existing examples).
- Maintain coding style (pep8 or black).

Feel free to open an issue for any feature request, question, or bug report.

## License

This project is distributed under the terms specified in the LICENSE file (if provided). If not provided, please consult the repository owner for the exact license details.

---

Thank you for your interest in the LLM Agent Framework. We hope it accelerates your AI-driven workflows and inspires new ways to leverage LLMs in your own projects!
