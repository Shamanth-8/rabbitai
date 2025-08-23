import openai

openai.api_key = "YOUR_OPENAI_KEY"

def explain_code(code: str, analysis: dict):
    prompt = f"""
    Analyze the following Python code:
    {code}

    Static analysis:
    {analysis}

    Tasks:
    1. Summarize what the code does.
    2. Suggest improvements.
    3. Recommend learning topics.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )
    return response["choices"][0]["message"]["content"]
