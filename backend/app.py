from fastapi import FastAPI, UploadFile, Form, HTTPException
import google.generativeai as genai
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Handle imports for different running contexts
try:
    # When running as a module (uvicorn backend.app:app)
    from .analyzer import analyze_code
    from .ai_helper import explain_code
except ImportError:
    # When running directly from backend directory
    from analyzer import analyze_code
    from ai_helper import explain_code

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

app = FastAPI()
genai.configure(api_key=API_KEY)

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
    try:
        if not file.filename.endswith(('.py', '.txt')):
            raise HTTPException(status_code=400, detail="Only Python and text files are allowed")
        
        code = (await file.read()).decode("utf-8")
        analysis = analyze_code(code)
        ai_insights = explain_code(code, analysis, problem=problem, level=level)

        return {
            "problem": problem,
            "level": level,
            "analysis": analysis,
            "ai_insights": ai_insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/code-bunny")
async def talk_to_code_bunny(req: BunnyRequest):
    try:
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

        # Try different possible API methods
        try:
            # Method 1: Try generate_content (newer versions)
            response = genai.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[m["content"] for m in messages]
            )
            reply = response.text
        except AttributeError:
            try:
                # Method 2: Try generate_text (older versions)
                response = genai.generate_text(
                    model="gemini-2.0-flash-exp",
                    prompt="\n".join([m["content"] for m in messages])
                )
                reply = response.text
            except AttributeError:
                try:
                    # Method 3: Try the most basic approach
                    model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    response = model.generate_content("\n".join([m["content"] for m in messages]))
                    reply = response.text
                except Exception as e:
                    reply = f"Error with AI generation: {str(e)}"

        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code Bunny request failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Code Bunny Backend...")
    print("🌐 Backend will be available at: http://127.0.0.1:8000")
    print("📚 API docs will be available at: http://127.0.0.1:8000/docs")
    print("Press Ctrl+C to stop the server")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
