import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("google.gemini.api-key")
MODEL = os.getenv("google.gemini.model", "gemini-2.5-flash")

client = genai.Client(api_key=API_KEY)


def analyze_resume(resume_text, user_goal):
    prompt = f"""
You are a senior software engineer and hiring manager.

Return ONLY valid JSON.
Do not use markdown.
Do not use ```json.
Do not add explanation text.

Return exactly this format:

{{
  "skills": [],
  "missing_skills": [],
  "roadmap": [],
  "interview_questions": []
}}

Resume:
{resume_text}

Goal:
{user_goal}
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        content = response.text.strip()

        # Extract JSON safely
        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("No valid JSON returned from Gemini.")

        json_content = content[start:end + 1]

        return json.loads(json_content)

    except Exception as e:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }