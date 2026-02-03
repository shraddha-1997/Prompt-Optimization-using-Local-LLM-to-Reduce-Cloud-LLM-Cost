

from langgraph.graph import StateGraph
from optimizer.optimizer_node import optimize_prompt
#from groq.groq_node import call_groq
from groq_node_pkg.groq_node import call_groq

# STAGE 2 GRAPH (optimizer only)

stage2_builder = StateGraph(dict)
stage2_builder.add_node("optimizer", optimize_prompt)
stage2_builder.set_entry_point("optimizer")
stage2_builder.set_finish_point("optimizer")
stage2_graph = stage2_builder.compile()


# STAGE 3 GRAPH (Groq only)

stage3_builder = StateGraph(dict)
stage3_builder.add_node("groq", call_groq)
stage3_builder.set_entry_point("groq")
stage3_builder.set_finish_point("groq")
stage3_graph = stage3_builder.compile()
