# Overview

This README explains how to customize prompt strings in different parts of the framework. The Agent framework includes:

1. **Agent**:

- Capable of direct single-step execution (execute_prompt).
- Final result summarizing (summary_prompt).

2. **Planner** (e.g., GenericPlanner):

- Creates a multi-step plan (prompt).

3. **evaluator** (e.g., GenericEvaluator):

- Evaluates correctness or quality of LLM output (prompt).

By overriding these prompts, developers can tailor the output style, instructions, or constraints for each step in the agent’s workflow. Customizing these prompts only affects the current instance of Agent, Planner, or evaluator and does not persist globally (i.e., creating a new Agent() reverts to default prompts).

# Capabilities at a Glance

1. **Override GenericEvaluator Prompt**

- By default, GenericEvaluator checks multiple criteria (accuracy, relevance, etc.).
- You can change it to check grammar only, or other specialized concerns, by setting its .prompt.

2. **Override Agent Single-Step Prompt** (execute_prompt)

- Controls how the agent handles a direct, single-step LLM call without a planner.
- Variables available: {task}, {background}, and (if you wish) {context_section}.

3. **Override Planner Prompt** (planner.prompt)

- Controls how tasks are broken down into steps.
- Variables typically include {task}, {tools_knowledge}, {knowledge}, possibly others (like {example_json1}, {example_json2} in GenericPlanner).

4. **Override Agent Summary Prompt** (summary_prompt)

- Controls how the final step-by-step history is summarized.
- You can shape the final “report” or “explanation” given to the user.

#### Important:

- You cannot add new placeholders to the built-in prompts (like "{myCustomVar}"), because the system only supports the existing placeholders recognized in each prompt’s .format(...) call.
- These overrides are instance-specific; if you create a new Agent or Planner, the default prompts will be restored.

# Step-by-Step Instructions to Override Prompts

1. **Initialize and Configure the Agent**

```python
from agent_core.agents import Agent

# Create agent instance
agent = Agent()
# Optionally set agent.background for context
agent.background = "I am a helpful assistant."
```

2. **Override the Agent’s Single-Step Prompt**

```python
print("Default Agent Execution Prompt:\n", agent.execute_prompt)
agent.execute_prompt = (
    "Customized single-step prompt.\n"
    "Task: {task}\n"
    "Background: {background}\n"
)
```

3. **Override the Final Summary Prompt**

```python
print("Default Agent Summary Prompt:\n", agent.summary_prompt)
agent.summary_prompt = "Here is a custom summary for steps:\n{history_text}"
```

4. **Use a Planner (e.g. GenericPlanner) and Override Its Prompt**

```python
from agent_core.planners.generic_planner import GenericPlanner

planner = GenericPlanner()
print("Default Planner Prompt:\n", planner.prompt)
planner.prompt = """\
I only want two simple steps:
Task: {task}
Tools: {tools_knowledge}
Output JSON with two main steps.
"""
agent.planner = planner  # Attach to the agent
```

5. **Override a evaluator Prompt (e.g. Scoreevaluator)**

```python
from agent_core.evaluator import GenericEvaluator

evaluator = GenericEvaluator()
print("Default evaluator Prompt:\n", evaluator.prompt)

# Custom grammar-only evaluator prompt
evaluator.prompt = """\
You are a special evaluator focusing on only grammar correctness.
Subtask: {request}
Output: {response}
Please check grammar only.
"""
```

6. **Run the Agent**

```python
result = agent.execute("draw a flower")
print("Execution result:", result)
print("Final Summary:\n", agent.get_execution_result_summary())
```

# Effects and Scope

- Overridden Prompts are local to the current objects: agent, planner, evaluator.
- Once you destroy or re-initialize them (agent = Agent()), the defaults are restored.
- If you want to keep your overrides, re-apply them each time you create a new instance.

# Example Code Walkthrough

example9.py demonstrates these capabilities:

1. Set Config.set_log_level("DEBUG") to see detailed logs.
2. Create a new Scoreevaluator, override prompt to check grammar only.
3. Create a new Agent, override the single-step execute_prompt.
4. Create a GenericPlanner, override the prompt to produce only two steps.
5. Execute the agent with a custom environment.
6. Override the agent’s summary_prompt and retrieve a final summary.

# Conclusion

By following the pattern in example9.py, you can flexibly:

- Define how each evaluator judges outputs.
- Shape how each Agent either runs tasks directly or uses a Planner.
- Customize the final summary generation.

Use these overrides for one-off tasks or for specialized flows in your application. Remember to re-apply if you recreate objects. This approach gives you fine-grained control while keeping the default framework intact.
