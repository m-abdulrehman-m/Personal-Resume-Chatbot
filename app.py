import os
from flask import Flask, request, jsonify, send_file
import requests

app = Flask(__name__)

# ---------- YOUR FULL RESUME (exactly from the document) ----------
RESUME_CONTEXT = """
Abdul Rehman

Computer Science Student & Founder, Codveon

YOUR_EMAIL | YOUR_LINKEDIN_URL | YOUR_GITHUB_URL | https://codveon.com | Lahore, Pakistan

PROFESSIONAL SUMMARY
Computer Science student at UET Lahore and founder of Codveon, a software development company offering web apps, mobile apps, desktop software and general IT services for local Pakistani businesses and international clients.
(TODO: apni 2-3 line ki summary yahan likho)

TECHNICAL SKILLS
Languages: (TODO)
Frameworks / Libraries: (TODO)
Databases: (TODO)
Dev Tools: Git, GitHub (TODO: baqi tools add karo)

EXPERIENCE
Founder (YEAR -- Present) - Codveon
- (TODO: Codveon mein kya kaam kiya / kya services deen)

PROJECTS
- (TODO: Project name) (YEAR)
  Tech stack: (TODO)
  - (TODO: kya banaya, kya result mila)

EDUCATION
Bachelor of Science in Computer Science (YEAR -- Present) - University of Engineering and Technology (UET), Lahore, Pakistan
- Relevant Coursework: (TODO)

CERTIFICATIONS & LEARNING
- (TODO)
"""

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = f"""You are an AI assistant named "Abdul's Resume Assistant". Your only knowledge source is the resume of Abdul Rehman provided below. Answer all user questions exclusively using the information from that resume. If the question cannot be answered from the resume, politely say that the information is not available in the resume and suggest asking about his skills, projects, experience, education, or certifications. Be helpful, concise, and friendly.

RESUME CONTENT:
{RESUME_CONTEXT}"""

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return "", 200
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Resume Chatbot"
    }
    payload = {
        "model": "qwen/qwen3-235b-a22b",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }
    try:
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        if resp.status_code != 200:
            return jsonify({"error": f"AI service error: {resp.status_code}"}), 502
        result = resp.json()
        reply = result["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
