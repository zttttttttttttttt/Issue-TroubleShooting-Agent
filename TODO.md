# TODO

### Feature
- execution bug: 
1) if step B successful, prvious step A is removed in the execution prompt
2) should remove Previous Step Failed Attempt record in context
- replan bug
1) plan_graph.tools_knowledge is missing when replanning
- compatible with autogen and langgraph
- validation retry in generic planner(v1)
- summary include agent execute result(v1)
- execute: background, context, tool (v1)
- evaluator: background, context (v1)
- tool execute try catch exception add evaluator, add suggestion (v1)
- replan: background, knowledge, categories_str, task, tool (background, knowledge, categories_str, task, tool) (v1)

- change context by step(v2)
- enrich log (input/output/prompt)(v2)
- knowledge & background rag (v2)
- support overwrite validation max attempt and threshold(v2)
- knowledge graph to collect sufficient information(v2)

### Test
- more unit testing

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
- UI interaction
- pass parent task for all step execution 
- fix background used in planner
- validation add execution history 
- expose generic planner prompt from graph planner 
- change validator to evaluator
- abstract validator base, unique output return
- adjust planner prompt to use tool better
- bug (done)
```json
{
     "id": "B.2.1.1.2",
     "task_description": "Select the right wing emoji characters for the dragon, focusing on specific styles and sizes.",
     "next_nodes": ["B.3"],
     "validation_threshold": 0.9,
     "max_attempts": 3
}
```