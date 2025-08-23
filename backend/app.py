from fastapi import FastAPI, UploadFile
from analyzer import analyze_code
from ai_helper import explain_code

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile):
    code = (await file.read()).decode("utf-8")
    
    analysis = analyze_code(code)
    ai_insights = explain_code(code, analysis)
    
    return {
        "analysis": analysis,
        "ai_insights": ai_insights
    }
