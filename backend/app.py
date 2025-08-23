from fastapi import FastAPI, UploadFile, Form
from analyzer import analyze_code
from ai_helper import explain_code
from google import genai
from pydantic import BaseModel

app = FastAPI()
client = genai.Client(api_key="AIzaSyA0XnXAO4N3hVSvDGSMSw2qZ0XLqiH29jo")

class BunnyRequest(BaseModel):
    analysis_result: dict
    chat_history: list  # list of {"role": "user"/"assistant", "content": "text"}
    user_prompt: str

@app.post("/analyze")
async def analyze(
    file: UploadFile,
    problem: str = Form(...),
    level: str = Form(...)
):
    code = (await file.read()).decode("utf-8")
    analysis = analyze_code(code)
    ai_insights = explain_code(code, analysis, problem=problem, level=level)

    return {
        "problem": problem,
        "level": level,
        "analysis": analysis,
        "ai_insights": ai_insights
    }

@app.post("/code-bunny")
async def talk_to_code_bunny(req: BunnyRequest):
    # Build a conversational history
    messages = [
        {"role": "system", "content": "You are Code Bunny 🐇✨, a playful yet smart coding assistant. Be concise but helpful."},
        {"role": "system", "content": f"Here is the code analysis context: {req.analysis_result}"}
    ]

    # Add past conversation
    for msg in req.chat_history:
        messages.append(msg)

    # Add the new user prompt
    messages.append({"role": "user", "content": req.user_prompt})

    # Call Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[m["content"] for m in messages]
    )

    return {"reply": response.text}
