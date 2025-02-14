# TODO

### Feature
- knowledge graph to collect sufficient information
- change context by step  (done?)
- validation retry in generic planner
- change validator to evaluator (done)
- generic model creation and config (done)
- fix background used in planner (done)
- expose generic planner prompt from graph planner (done)
- validation add execution history (done)
- abstract validator base, unique output return  (done)
- pass parent task for all step execution  (done)
- adjust planner prompt to use tool better  (done)
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
- unit testing
- 
### UI
- UI interaction

### Doc
- read me for each example
- how to debug in the library?
- add R2D2 in readme
- add FAQ section

# Completed
- stream processing for each step during the execution
- step validator by category, support costomized
- history planning experience for improving
- successful geratation rate
- put example in another project
