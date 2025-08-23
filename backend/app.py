from fastapi import FastAPI, UploadFile, Form
from analyzer import analyze_code
from ai_helper import explain_code

app = FastAPI()

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
