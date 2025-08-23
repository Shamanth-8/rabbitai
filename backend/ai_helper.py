from google import genai

client = genai.Client(api_key="AIzaSyBQ2qaFxiWx8VG2VRbk6VNuGqrtbQvALB4")


def explain_code(code: str, analysis: dict, problem: str, level: str):
    prompt = f"""
    Analyze the following Python code:
    {code}

    Static analysis:
    {analysis}

    Tasks:
    1. Summarize what the code does.
    2. Suggest improvements.
    3. Recommend learning topics.

    This is for {level} level users and the problem is {problem}
    """

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt)
    return response.text
