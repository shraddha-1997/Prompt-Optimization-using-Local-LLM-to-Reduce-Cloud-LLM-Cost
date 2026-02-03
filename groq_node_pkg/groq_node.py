import os
from groq import Groq

#client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def get_groq_client():
    from groq import Groq
    import os

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set")

    return Groq(api_key=api_key)


def call_groq(state):
    client = get_groq_client()

    response = client.chat.completions.create(
        #model="llama3-8b-8192",
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": state["optimized_query"]}
        ]
    )

    return {
        "final_response": response.choices[0].message.content
    }



'''
def call_groq(state: dict) -> dict:
    optimized_query = state["optimized_query"]

    completion = client.chat.completions.create(

	model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": optimized_query}
        ],
        temperature=0.2,
    )

    final_answer = completion.choices[0].message.content

    state["final_response"] = final_answer
    print("USING KEY:", os.getenv("GROQ_API_KEY")[:6])
    print("GROQ EXECUTED")

    return state
'''
