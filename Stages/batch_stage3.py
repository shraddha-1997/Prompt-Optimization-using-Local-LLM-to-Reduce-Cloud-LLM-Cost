
import pandas as pd
from graph import graph

# Load Stage 2 results
df = pd.read_csv("stage2.1_prompt_optimization_results.csv")

stage3_results = []

for _, row in df.iterrows():
    # Invoke LangGraph with optimized query
    output = graph.invoke({
        "optimized_query": row["optimized_query"]
    })

    stage3_results.append({
        "query_id": row["query_id"],
        "original_query": row["original_query"],
        "optimized_query": row["optimized_query"],
        "final_response": output["final_response"]
    })

# Convert to DataFrame
stage3_df = pd.DataFrame(stage3_results)

# Save results
stage3_df.to_csv("stage3.1.1_final_responses.csv", index=False)

print(" Stage 3 completed successfully. Results saved to stage3_final_responses.csv")


'''
import pandas as pd
from graph import graph

# Load Stage 2 results
df = pd.read_csv("stage2.1_prompt_optimization_results.csv")

stage3_results = []

for _, row in df.iterrows():
    # Call LangGraph using optimized query
    output = graph.invoke({
        "optimized_query": row["optimized_query"]
    })

    stage3_results.append({
        "query_id": row["query_id"],
        "original_query": row["original_query"],
        "optimized_query": row["optimized_query"],
        "original_tokens": row["original_tokens"],
        "optimized_tokens": row["optimized_tokens"],
        "token_reduction_%": row["token_reduction_%"],
        "final_response": output["final_response"]
    })

# Convert to DataFrame
stage3_df = pd.DataFrame(stage3_results)

# Save results
stage3_df.to_csv("stage3.1_final_responses.csv", index=False)

print("✅ Stage 3 completed successfully. Results saved to stage3.1_final_responses.csv")


'''
