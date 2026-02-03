import json
import pandas as pd
#from graph import graph
from graph import stage2_graph as graph
from optimizer.token_utils import count_tokens
MAX_QUERIES = 10
results = []
with open("data/queries.json", "r") as f:
    for i, line in enumerate(f):
        if i >= MAX_QUERIES:
            break
        query_data = json.loads(line)
        original_text = query_data["text"]

        # 1. Invoke the graph using the key your Node expects  This triggers existing optimizer_node logic and templates
        output = graph.invoke({
            "user_prompt": original_text
        })

        # 2. Get the result from your Node's 'final_response' key
        #optimized_text = output.get("final_response", original_text).strip()
        optimized_text = output.get("optimized_prompt", original_text).strip()

        # 3. Calculate tokens manually here so the CSV isn't all zeros
        orig_tokens = count_tokens(original_text)
        opt_tokens = count_tokens(optimized_text)

        # 4. Calculate reduction percentage
        if orig_tokens > 0:
            token_reduction = ((orig_tokens - opt_tokens) / orig_tokens * 100)
        else:
            token_reduction = 0.0

        # Safety: Use original if optimization somehow made it longer
        final_query = optimized_text if token_reduction >= 0 else original_text
        final_tokens = opt_tokens if token_reduction >= 0 else orig_tokens
        reduction_val = round(token_reduction, 2) if token_reduction >= 0 else 0.0

        results.append({
            "query_id": query_data["_id"],
            "original_query": original_text,
            "optimized_query": final_query,
            "original_tokens": orig_tokens,
            "optimized_tokens": final_tokens,
            "token_reduction_%": reduction_val
        })

df = pd.DataFrame(results)
df.to_csv("stage2.1.1_prompt_optimization_results.csv", index=False)

print("Stage 2 completed using existing Node and Template logic.")
