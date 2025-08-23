import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=API_KEY)

def explain_code(code: str, analysis: dict, problem: str, level: str):
    try:
        prompt = f"""
        Analyze the following Python code:
        {code}

        Static analysis:
        {json.dumps(analysis, indent=2)}

        Tasks:
        1. Summarize what the code does.
        2. Suggest improvements.
        3. Recommend learning topics.

        This is for {level} level users and the problem is {problem}
        """

        # Try different possible API methods
        try:
            # Method 1: Try generate_content (newer versions)
            response = genai.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt
            )
            return response.text
        except AttributeError:
            try:
                # Method 2: Try generate_text (older versions)
                response = genai.generate_text(
                    model="gemini-2.0-flash-exp",
                    prompt=prompt
                )
                return response.text
            except AttributeError:
                try:
                    # Method 3: Try the most basic approach
                    model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    response = model.generate_content(prompt)
                    return response.text
                except Exception as e:
                    return f"Error with AI generation: {str(e)}"
            
    except Exception as e:
        return f"Error generating AI insights: {str(e)}"