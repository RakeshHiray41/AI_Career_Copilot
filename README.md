# 🚀 AI Career Copilot

AI Career Copilot is an intelligent resume analyzer built using Flask and Google Gemini AI. It helps users analyze their resumes, identify missing skills, generate learning roadmaps, and prepare for interviews.

---

# ✨ Features

- 🔐 User Authentication (Signup/Login)
- 📄 Upload Resume (PDF/DOCX)
- 📝 Paste Resume Text
- 🤖 AI-Powered Resume Analysis using Gemini
- 🎯 Goal-Based Skill Analysis
- 📚 Missing Skills Detection
- 🛣️ Personalized Learning Roadmap
- 💡 Interview Question Generation
- 📊 Analysis History
- 🗑️ Delete Previous Reports
- 🎨 Modern Responsive UI

---

# 🛠️ Tech Stack

## Backend
- Python
- Flask
- SQLAlchemy
- PyMySQL
- Flask-Bcrypt

## AI
- Google Gemini API
- Gemini 2.5 Flash

## Database
- TiDB Cloud (MySQL)

## Frontend
- HTML
- CSS
- Jinja2

---

# 📂 Project Structure

```bash
AI_CAREER_COPILOT/
│
├── app.py
├── db.py
├── models.py
├── requirements.txt
├── .env
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   └── history.html
│
├── static/
│   └── style.css
│
├── uploads/
└── venv/
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/AI_CAREER_COPILOT.git
cd AI_CAREER_COPILOT
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash

DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@HOST:4000/test

SSL_CERT_PATH=C:\path\to\isrgrootx1.pem
```

---

# 🗄️ Database Configuration

Example:

```python
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl": {
            "ca": SSL_CERT_PATH
        }
    }
)
```

---

# ▶️ Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 🤖 AI Analysis Output

The application generates:

```json
{
  "skills": [],
  "missing_skills": [],
  "roadmap": [],
  "interview_questions": []
}
```

---

# 📄 Resume Formats Supported

- PDF
- DOCX
- Plain Text

---

# 📸 Screenshots

## Dashboard
- Upload Resume
- Paste Resume
- Enter Career Goal
- Analyze Resume

## History
- View Previous Reports
- Delete Reports

---

# 🔒 Security

- Password hashing using Flask-Bcrypt
- Environment variables for secrets
- SSL connection to TiDB Cloud
- .gitignore for API keys and certificates

---

# 📦 Requirements

```text
Flask
Flask-Bcrypt
SQLAlchemy
PyMySQL
python-dotenv
google-genai
PyPDF2
python-docx
```

Install:

```bash
pip install Flask Flask-Bcrypt SQLAlchemy PyMySQL python-dotenv google-genai PyPDF2 python-docx
```

---

# 🚀 Future Enhancements

- Resume ATS Score
- Resume Suggestions
- Skill Gap Charts
- Email Reports
- Download PDF Reports
- Resume Templates
- LinkedIn Integration
- Job Recommendations

---

# 👨‍💻 Author

## Rakesh Hiray

- Master's in Computer Science
- Python Developer
- Backend Developer
- Flask & FastAPI Enthusiast

---

# ⭐ If you like this project

Please give it a ⭐ on GitHub.

---

Made with ❤️ by Rakesh Hiray