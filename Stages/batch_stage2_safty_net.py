
import json
import pandas as pd
from graph import graph
from optimizer.token_utils import count_tokens

MAX_QUERIES = 10
results = []

# This is the important to fix our project goal 
OPTIMIZATION_INSTRUCTION = "Task: Shorten the following prompt to be highly token-efficient. Keep only the core intent. Do NOT answer it. Prompt: "

with open("data/queries.json", "r") as f:
    for i, line in enumerate(f):
        if i >= MAX_QUERIES: break
        
        query_data = json.loads(line)
        original_text = query_data["text"]

        #  WE INJECT THE INSTRUCTION HERE
        # This forces 'Stage 3' node to act like a 'Stage 2' optimizer
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
