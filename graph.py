from langgraph.graph import StateGraph
from optimizer.optimizer_node import optimize_prompt

# Define graph state schema
graph_builder = StateGraph(dict)

graph_builder.add_node("optimizer", optimize_prompt)
graph_builder.set_entry_point("optimizer")
graph_builder.set_finish_point("optimizer")

graph = graph_builder.compile()
