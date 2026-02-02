from typing import TypedDict
import tiktoken

from langgraph.graph import StateGraph
from langchain_ollama import OllamaLLM

# 1. Define LangGraph State
class PromptState(TypedDict):
    user_prompt: str
    optimized_prompt: str
    original_tokens: int
    optimized_tokens: int


# 2. Token Counter
def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    encoder = tiktoken.encoding_for_model(model)
    return len(encoder.encode(text))



# 3. Prompt Optimization Node
def optimize_prompt(state: PromptState) -> dict:
    llm = OllamaLLM(model="mistral")

    with open("optimizer_prompt.txt", "r") as f:
        system_prompt = f.read()

    prompt = f"""
{system_prompt}

Input:
{state['user_prompt']}

Optimized:
"""

    optimized = llm.invoke(prompt).strip()

    return {
        "optimized_prompt": optimized,
        "original_tokens": count_tokens(state["user_prompt"]),
        "optimized_tokens": count_tokens(optimized),
    }


# 4. Build LangGraph Workflow
workflow = StateGraph(PromptState)

workflow.add_node("optimize", optimize_prompt)
workflow.set_entry_point("optimize")

graph = workflow.compile()


# 5. Run the System 
if __name__ == "__main__":
    user_prompt = """
    I am a retail investor and I would like to understand how inflation
    affects bond prices in the long term. Please explain this clearly
    with suitable examples.
    """

    result = graph.invoke({"user_prompt": user_prompt})

    print("\n--- ORIGINAL PROMPT ---")
    print(user_prompt.strip())

    print("\n--- OPTIMIZED PROMPT ---")
    print(result["optimized_prompt"])

    print("\n--- TOKEN STATS ---")
    print("Original Tokens :", result["original_tokens"])
    print("Optimized Tokens:", result["optimized_tokens"])
    print(
        "Reduction (%)   :",
        round(
            (result["original_tokens"] - result["optimized_tokens"])
            / result["original_tokens"] * 100,
            2
        )
    )
