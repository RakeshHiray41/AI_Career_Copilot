from flask import Flask, redirect, render_template, request, session
from flask_bcrypt import Bcrypt
from db import engine, Base, sessionLocal
from models import User, Report
import PyPDF2
import docx
import json
import os

from dotenv import load_dotenv
from google import genai

# ---------------- GEMINI CONFIG ----------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=API_KEY)

# ---------------- FLASK APP ----------------
app = Flask(__name__)
app.secret_key = "rakesh123"

bcrypt = Bcrypt(app)

Base.metadata.create_all(bind=engine)


# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    db = sessionLocal()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = db.query(User).filter_by(
            email=email
        ).first()

        if existing_user:
            return "User already exists"

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        new_user = User(
            email=email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()

        return redirect("/login")

    return render_template("signup.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    db = sessionLocal()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = db.query(User).filter_by(
            email=email
        ).first()

        if user and bcrypt.check_password_hash(
            user.password,
            password
        ):
            session["user"] = user.email
            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")


# ---------------- AI FUNCTION ----------------
def analyze_resume(resume_text, user_goal):
    prompt = f"""
You are a senior software engineer and hiring manager.

Evaluate the resume based on the user's goal.

User Goal: "{user_goal}"

STRICT RULES:
- Extract only relevant skills for this goal.
- Remove irrelevant tools.
- Generate roadmap only for missing skills.
- Generate interview questions.

Return ONLY valid JSON:

{{
    "skills": [],
    "missing_skills": [],
    "roadmap": [],
    "interview_questions": []
}}

Resume:
{resume_text}
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        content = response.text.strip()

        print("Gemini Response:")
        print(content)

        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                "No valid JSON returned from Gemini."
            )

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


# ---------------- DASHBOARD ----------------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":
        user_goal = request.form.get("role")
        resume_text = request.form.get("resume", "")

        file = request.files.get("file")

        # PDF Upload
        if file and file.filename != "":
            if file.filename.endswith(".pdf"):
                try:
                    pdf_reader = PyPDF2.PdfReader(file)

                    text = ""

                    for page in pdf_reader.pages:
                        text += (
                            page.extract_text() or ""
                        )

                    resume_text = text

                except Exception as e:
                    result = {
                        "error":
                        f"PDF Error: {str(e)}"
                    }

            # DOCX Upload
            elif file.filename.endswith(".docx"):
                try:
                    doc = docx.Document(file)

                    text = ""

                    for para in doc.paragraphs:
                        text += para.text + "\n"

                    resume_text = text

                except Exception as e:
                    result = {
                        "error":
                        f"DOCX Error: {str(e)}"
                    }

        if resume_text and user_goal:
            try:
                result = analyze_resume(
                    resume_text,
                    user_goal
                )

                

                db = sessionLocal()

                user = db.query(User).filter_by(
                    email=session["user"]
                ).first()

                report = Report(
                    user_id=user.id,
                    resume_text=resume_text,
                    result=json.dumps(result)
                )

                db.add(report)
                db.commit()

            except Exception as e:
                result = {
                    "error":
                    f"AI Error: {str(e)}"
                }

    return render_template(
        "dashboard.html",
        user=session["user"],
        result=result
    )


# ---------------- HISTORY ----------------
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")

    db = sessionLocal()

    user = db.query(User).filter_by(
        email=session["user"]
    ).first()

    reports = db.query(Report).filter_by(
        user_id=user.id
    ).all()

    parsed_reports = []

    for r in reports:
        try:
            parsed_result = json.loads(r.result)
        except:
            parsed_result = {}

        parsed_reports.append({
        "id": r.id,
        "resume": r.resume_text,
        "result": parsed_result
})

    return render_template(
        "history.html",
        reports=parsed_reports
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


@app.route("/delete-history/<int:report_id>")
def delete_history(report_id):
    if "user" not in session:
        return redirect("/login")

    db = sessionLocal()

    user = db.query(User).filter_by(
        email=session["user"]
    ).first()

    report = db.query(Report).filter_by(
        id=report_id,
        user_id=user.id
    ).first()

    if report:
        db.delete(report)
        db.commit()

    return redirect("/history")

if __name__ == "__main__":
    app.run(debug=True)
