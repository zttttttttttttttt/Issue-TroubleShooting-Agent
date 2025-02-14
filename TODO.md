# TODO
- pass parent task for all step execution
- fix background used in planner
- validation add execution history
- compatible with autogen and langgraph
- expose generic planner prompt from graph planner
- add R2D2 in readme
- add FAQ section
- read me for each example
- change context by step
- how to debug in the library?
- validation retry in generic planner
- change validator to evaluator
- abstract validtor base, unique output return
- adjust planner pronpt to use tool better
- more unit testing
- knowledge graph to collect sufficient informaiton
- UI interaction
- bug
```json
{
     "id": "B.2.1.1.2",
     "task_description": "Select the right wing emoji characters for the dragon, focusing on specific styles and sizes.",
     "next_nodes": ["B.3"],
     "validation_threshold": 0.9,
     "max_attempts": 3
}
```

# Completed
- generic model creation and config
- stream processing for each step during the execution
- step validator by category, support costomized
- history planning experience for improving
- successful geratation rate
- put example in another project
