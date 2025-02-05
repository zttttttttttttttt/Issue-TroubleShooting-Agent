# PhAENix - LLM Agent Development Framework

This framework is an advanced yet user-friendly platform for developing LLM-based agents, integrating task planning, validation, and execution into a seamless workflow. It abstracts complex aspects like prompt engineering, multi-model coordination, and operational flow management, enabling developers to quickly create agents without overwhelmed by technical complexities. With a flexible design, it supports a wide range of use cases while providing users with fine-grained control over each component.

- **Developer-Friendly**: By hiding most of the underlying complexity, this framework makes it straightforward for developers to specify high-level goals such as planning steps and configuring validation without worrying about convoluted implementation details.
- **Planner Variety**: The framework offers flexible planning options, including step-based planners like GenericPlanner and more complex node-graph planners like GraphPlanner, ensuring that both simple and intricate workflows are supported seamlessly.
- **Validation Architecture**: It includes a robust validation system that checks outputs at every step, allowing errors to be detected early. This iterative validation significantly enhances overall accuracy by ensuring that tasks are iteratively refined or dynamically adjusted.
- **Custom Configuration**: Users can adjust the framework to use different LLM models for different components—such as planning, validation, or execution—allowing precise control over the agent's behavior. Additionally, customizing prompts for each module allows for specific and tailored interactions at each stage.
- **Tool & Ul Integration**: The framework supports dynamic tool use and integration with external APls. Developers can call functions, engage in real-time interactions, or retrieve live data as part of the agent's workflow, enabling interactive scenarios and adaptive behavior.

In summary, this LLM agent framework offers the perfect balance between abstraction and customization, empowering developers to create powerful, intelligent agents with minimal effort while ensuring flexibility and precision in every step.

---

PhAENix is a variant and draws inspiration from the Phoenix, a mythical creature symbolizing rebirth, wisdom, and excellence across cultures.
The embedded AEN represents the core traits of an Agent: adaptability, evolution and nexus, highlighting the modern and innovative nature of the framework.

- **A**: Stands for Adaptability, highlighting the LLM Agent’s ability to dynamically adjust and perform well in various scenarios and tasks.
- **E**: Represents Evolution, emphasizes the self-optimization and iterative capabilities of the LLM Agent, symbolizing continuous transformation and improvement.
- **N**: Refers to Nexus, highlighting the LLM Agent’s role as a bridge between humans and knowledge, as well as humans and technology.

PhAENix seamlessly integrates the mythical rebirth of the Phoenix with the LLM Agent’s core strengths, showcasing its adaptability, self-evolution, and ability to empower users by automating repetitive tasks.

---

## Table of Contents

1. [Installation](#installation)

---

## Installation

#### 1. Clone the repository

```bash
git clone https://github.com/lukewu8023/agent-core.git
```

#### 2. Create you own agent repository

```bash
mkdir x-agent
cd x-agent
```

#### 3. (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### 3. Install the project as a library

You can install by referencing the directory:

```bash
pip install -e path/to/agent-core
```

This will make the agents, planners, models, etc. available in your Python environment.