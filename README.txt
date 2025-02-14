# PhAENix - Single LLM Agent Development Framework

PhAENix is an advanced, developer-friendly framework for building **single reliable LLM-based autonomous agents**, integrating **task planning**, **evaluation**, and **execution** into a seamless workflow. It abstracts complex aspects such as prompt engineering, multi-model coordination, and operational flow management—enabling developers to create powerful agents without being overwhelmed by technical intricacies. With a flexible design, PhAENix supports a wide range of use cases while allowing fine-grained control over each component.

- **Developer-Friendly**: By hiding most of the underlying complexity, this framework makes it straightforward for developers to specify high-level goals such as planning steps and configuring evaluation without worrying about convoluted implementation details.
- **Planner Variety**: The framework offers flexible planning options, including step-based planners like GenericPlanner and more complex node-graph planners like GraphPlanner, ensuring that both simple and intricate workflows are supported seamlessly.
- **evaluation Architecture**: It includes a robust evaluation system that checks outputs at every step, allowing errors to be detected early. This iterative evaluation significantly enhances overall accuracy by ensuring that tasks are iteratively refined or dynamically adjusted.
- **Custom Configuration**: Users can adjust the framework to use different LLM models for different components—such as planning, evaluation, or execution—allowing precise control over the agent's behavior. Additionally, customizing prompts for each module allows for specific and tailored interactions at each stage.
- **Tool & Ul Integration**: The framework supports dynamic tool use and integration with external APls. Developers can call functions, engage in real-time interactions, or retrieve live data as part of the agent's workflow, enabling interactive scenarios and adaptive behavior.

In summary, this LLM agent framework offers the perfect balance between abstraction and customization, empowering developers to create powerful, intelligent agents with minimal effort while ensuring flexibility and precision in every step.

---

PhAENix is a variant and draws inspiration from the Phoenix, a mythical creature symbolizing rebirth, wisdom, and excellence across cultures.
The embedded AEN represents the core traits of an Agent: adaptability, evolution and nexus, highlighting the modern and innovative nature of the framework.

- **A**: Stands for Adaptability, highlighting the LLM Agent’s ability to dynamically adjust and perform well in various scenarios and tasks.
- **E**: Represents Evolution, emphasizes the self-optimization and iterative capabilities of the LLM Agent, symbolizing continuous transformation and improvement.
- **N**: Refers to Nexus, highlighting the LLM Agent’s role as a bridge between humans and knowledge, as well as humans and technology.

PhAENix seamlessly integrates the mythical rebirth of the Phoenix with the LLM Agent’s core strengths, showcasing its adaptability, self-evolution, and ability to empower users by automating repetitive tasks.

## Table of Contents

1. [Key Innovation Features](#key-innovation-features)
   - [Replan](#replan)
   - [Step evaluation](#step-evaluation)
   - [Percise Context Control](#percise-context-control)
2. [Comparison with Other Frameworks](#comparison-with-other-frameworks)
3. [Installation](#installation)
4. [Usage and Examples](#usage-and-examples)
5. [Feedback & Usage Tracking](#feedback--usage-tracking)

## Key Innovative Features

Below are some notable innovation highlights that set PhAENix apart. You can further expand each item with additional details, examples, or images to illustrate its capabilities.

### Replan

A concise description or tagline.  
_(Add more detailed explanations or images here.)_

### Step evaluation

A concise description or tagline.  
_(Add more detailed explanations or images here.)_

### Percise Context Control

A concise description or tagline.  
_(Add more detailed explanations or images here.)_

## Comparison with Other Frameworks

Below is a report comparing PhAENix with two other notable frameworks, **autogen** and **langgraph**, across several key features:

| Feature                               | **PhAENix**        | **AutoGen**  | **LangGraph** |
| ------------------------------------- | ------------------ | ------------ | ------------- |
| **Developer-Friendliness**            | ⭐️⭐️⭐️⭐️⭐️    | ⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️     |
| **Planner Variety (Step/Graph)**      | Yes (Multiple)     | Partial/Yes? | Partial/No?   |
| **Iterative evaluation Architecture** | Yes (Core Feature) | Yes/No?      | Yes/No?       |
| **Customizable LLM & Prompts**        | Fully Modular      | Yes/No?      | Yes/No?       |
| **Tool & UI Integration**             | Native Support     | Limited/No?  | Limited/No?   |

## Installation

#### 1. Clone the repository

```bash
git clone https://github.com/lukewu8023/agent-core.git
cd agent-core
```

#### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
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

## Usage and Examples

For a comprehensive set of examples demonstrating how to use PhAENix in various scenarios, please visit our **[agent-examples repository](https://github.com/lukewu8023/agent-examples)**. There you will find **detailed examples** that show how to:

- Integrate different planners ([Example 1](#))
- Configure and customize evaluation loops ([Example 2](#))
- Set up multiple LLMs for specific subtasks ([Example 3](#))

---

## Feedback & Usage Tracking

We value your feedback and would love to understand how you are using PhAENix. Here are some ways you can help us track and improve the project:

#### 1. Clone the Repository

- GitHub provides limited clone analytics, so if you’d like, please share your clone count or usage metrics by posting in GitHub issue ([Cloning Statistics](#)).

#### 2. Fork the Repository

- Use GitHub’s fork feature to create your own copy of the repo.
- This helps us track the number of active forks and gives us an idea of how many people are exploring or modifying PhAENix.

#### 3. Open a Usage Issue

- We have a dedicated Usage & Feedback Issue ([Usage Tracking](#)).
- Please drop by and let us know how you’re using PhAENix:
  - Are you simply testing or evaluating?
  - Have you deployed it in UAT or production environments?
  - Are you integrating it with other systems?

#### 4. Other Suggestions

- Stars & Watchers: Starring the repo and adding it to your watch list also gives us an indication of community interest.
- Pull Requests: Contribute features, fixes, or docs improvements. This helps us see real-world usage and encourages collaborative growth.

Your feedback is crucial for guiding the future development of PhAENix. Thank you for supporting and improving the framework!

---

Thank you for using PhAENix!  
If you have any questions or ideas for improvements, feel free to open an issue or contact the owner [Luke Wu](#).
