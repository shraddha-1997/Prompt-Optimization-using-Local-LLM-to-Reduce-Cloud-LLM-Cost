
from optimizer.prompt_templates import OPTIMIZER_SYSTEM_PROMPT
from optimizer.token_utils import count_tokens


from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="phi3:mini",
    temperature=0.0,
    max_tokens=50,  
    keep_alive="5m"
)


def optimize_prompt(state: dict) -> dict:
    user_prompt = state["user_prompt"]

    optimized_prompt = llm.invoke(
        f"{OPTIMIZER_SYSTEM_PROMPT}\n\nUser Query:\n{user_prompt}"
    )

    optimized_prompt = optimized_prompt.strip().split("\n")[0]

    return {
        "original_prompt": user_prompt,
        "optimized_prompt": optimized_prompt,
        "original_tokens": count_tokens(user_prompt),
        "optimized_tokens": count_tokens(optimized_prompt),
    }

