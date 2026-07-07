import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=API_KEY)


def analyze_resume(resume_text, user_goal):
    prompt = f"""
You are a senior software engineer and hiring manager.

Analyze the resume below against the candidate's goal.

Return the result strictly in this JSON structure:
{{
  "skills": [],
  "missing_skills": [],
  "roadmap": [],
  "interview_questions": []
}}

Rules:
- "skills": list of skills already present in the resume.
- "missing_skills": list of skills missing for the goal role.
- "roadmap": list of steps/topics to learn, in order.
- "interview_questions": list of likely interview questions for the goal role.

Resume:
{resume_text}

Goal:
{user_goal}
"""

    response = None
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=4096,
            ),
        )

        content = response.text.strip()

        result = json.loads(content)

        # Make sure all expected keys exist even if Gemini skips one
        for key in ["skills", "missing_skills", "roadmap", "interview_questions"]:
            if key not in result:
                result[key] = []

        return result

    except json.JSONDecodeError as e:
        raw_text = getattr(response, "text", "NO RESPONSE") if response else "NO RESPONSE OBJECT"
        print("JSON PARSE ERROR:", str(e))
        print("RAW GEMINI RESPONSE:", repr(raw_text))
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": f"JSON parse failed: {str(e)}"
        }

    except Exception as e:
        print("GEMINI CALL ERROR:", str(e))
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }