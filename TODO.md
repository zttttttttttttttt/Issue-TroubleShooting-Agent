# TODO

### Feature
- pass parent task for all step execution (done)
- fix background used in planner (done)
- validation add execution history (done)
- compatible with autogen and langgraph
- expose generic planner prompt from graph planner (done)
- change context by step  (done?)
- validation retry in generic planner
- change validator to evaluator (done)
- abstract validator base, unique output return (done)
- adjust planner prompt to use tool better (done)
- knowledge graph to collect sufficient information
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

### Test
- more unit testing
- 
### UI
- UI interaction

### Doc
- read me for each example
- how to debug in the library?
- add R2D2 in readme
- add FAQ section

# Completed
- generic model creation and config
- stream processing for each step during the execution
- step validator by category, support customized
- history planning experience for improving
- successful generation rate
- put example in another project
