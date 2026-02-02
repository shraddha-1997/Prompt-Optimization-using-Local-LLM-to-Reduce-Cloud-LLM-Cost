'''import json
import pandas as pd
from graph import graph

MAX_QUERIES = 5   # safe test limit
results = []

with open("data/queries.json", "r") as f:
    for i, line in enumerate(f):
        if i >= MAX_QUERIES:
            break

        query = json.loads(line)

        output = graph.invoke({
            "user_prompt": query["text"]
        })

        # Calculate token reduction %
        token_reduction = (
            (output["original_tokens"] - output["optimized_tokens"])
            / output["original_tokens"] * 100
        )

        # 🔒 SAFETY CHECK: Do not optimize if tokens increase
        if token_reduction < 0:
            final_optimized_query = output["original_prompt"]
            final_optimized_tokens = output["original_tokens"]
            token_reduction = 0.0
        else:
            final_optimized_query = output["optimized_prompt"]
            final_optimized_tokens = output["optimized_tokens"]

        results.append({
            "query_id": query["_id"],
            "original_query": output["original_prompt"],
            "optimized_query": final_optimized_query,
            "original_tokens": output["original_tokens"],
            "optimized_tokens": final_optimized_tokens,
            "token_reduction_%": round(token_reduction, 2)
        })

df = pd.DataFrame(results)
df.to_csv("stage2.1_prompt_optimization_results.csv", index=False)

print("Stage 2 completed successfully")

'''

'''
import json
import pandas as pd
from graph import graph

MAX_QUERIES = 5   # safe test limit
results = []

with open("data/queries.json", "r") as f:
    for i, line in enumerate(f):
        if i >= MAX_QUERIES:
            break

        query = json.loads(line)

        # 1. FIX THE INPUT KEY
        # Your node needs to receive the data it expects. 
        # If your node is currently set to read "optimized_query", 
        # we pass the text under that name.
        output = graph.invoke({
            "optimized_query": query["text"] 
        })

        # 2. FIX THE OUTPUT KEY ACCESS
        # In the file you showed me, your node returns "final_response".
        # We need to make sure we don't crash when calculating reduction.
        
        orig_tokens = output.get("original_tokens", 0)
        opt_tokens = output.get("optimized_tokens", 0)

        # Calculate token reduction % (with safety for zero division)
        if orig_tokens > 0:
            token_reduction = ((orig_tokens - opt_tokens) / orig_tokens * 100)
        else:
            token_reduction = 0.0

        # 🔒 SAFETY CHECK
        if token_reduction < 0:
            final_optimized_query = query["text"] # Fallback to original
            final_optimized_tokens = orig_tokens
            token_reduction = 0.0
        else:
            # Look for the result from your node
            final_optimized_query = output.get("final_response", query["text"])
            final_optimized_tokens = opt_tokens

        results.append({
            "query_id": query["_id"],
            "original_query": query["text"],
            "optimized_query": final_optimized_query,
            "original_tokens": orig_tokens,
            "optimized_tokens": final_optimized_tokens,
            "token_reduction_%": round(token_reduction, 2)
        })

df = pd.DataFrame(results)
df.to_csv("stage2.1_prompt_optimization_results.csv", index=False)

print("Stage 2 completed successfully")
'''


import json
import pandas as pd
from graph import graph
from optimizer.token_utils import count_tokens

MAX_QUERIES = 10
results = []

# This is the "Secret Sauce" to fix your project goal without touching the Node file
OPTIMIZATION_INSTRUCTION = "Task: Shorten the following prompt to be highly token-efficient. Keep only the core intent. Do NOT answer it. Prompt: "

with open("data/queries.json", "r") as f:
    for i, line in enumerate(f):
        if i >= MAX_QUERIES: break
        
        query_data = json.loads(line)
        original_text = query_data["text"]

        # 🚀 WE INJECT THE INSTRUCTION HERE
        # This forces your 'Stage 3' node to act like a 'Stage 2' optimizer
        forced_optimization_input = f"{OPTIMIZATION_INSTRUCTION} '{original_text}'"

        output = graph.invoke({
            "optimized_query": forced_optimization_input
        })

        # Capture the result (which should now be short)
        optimized_text = output.get("final_response", original_text).strip()

        # Calculate tokens
        orig_tokens = count_tokens(original_text)
        opt_tokens = count_tokens(optimized_text)

        # Calculate reduction
        token_reduction = ((orig_tokens - opt_tokens) / orig_tokens * 100) if orig_tokens > 0 else 0.0

        # Safety: If the LLM still failed and gave a long response, use the original
        if token_reduction < 0:
            final_query = original_text
            final_tokens = orig_tokens
            reduction_display = 0.0
        else:
            final_query = optimized_text
            final_tokens = opt_tokens
            reduction_display = round(token_reduction, 2)

        results.append({
            "query_id": query_data["_id"],
            "original_query": original_text,
            "optimized_query": final_query,
            "original_tokens": orig_tokens,
            "optimized_tokens": final_tokens,
            "token_reduction_%": reduction_display
        })

df = pd.DataFrame(results)
df.to_csv("stage2.1_prompt_optimization_results.csv", index=False)
print("SUCCESS: Your prompts are now being compressed!")
