# Personal Resume Chatbot

An AI-powered chatbot that answers questions about Abdul Rehman's resume. Visitors can ask about skills, projects, experience, education, and certifications, and the assistant responds using only the information provided in the resume.

The project consists of a Flask backend that connects to a large language model through the OpenRouter API, a single-page frontend, and an automated deployment pipeline built with GitHub Actions.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Deployment](#deployment)
- [Customization](#customization)
- [Limitations](#limitations)
- [Security Notes](#security-notes)
- [Author](#author)

---

## Features

- Answers questions strictly from the resume content provided in the system prompt
- Politely declines questions that fall outside the resume
- Lightweight REST API with a single chat endpoint
- Responsive single-page chat interface with no frontend build step
- Cross-origin (CORS) support for embedding the API in other sites
- Production-ready setup with Gunicorn and Nginx
- Fully automated deployment to an Ubuntu VPS on every push to `main`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Production server | Gunicorn, Nginx |
| AI provider | OpenRouter API (model: `qwen/qwen3-235b-a22b`) |
| Frontend | HTML, CSS, JavaScript |
| CI/CD | GitHub Actions |
| Hosting | Ubuntu VPS with systemd |

---

## Project Structure

```
Personal-resume-chatbot/
├── .github/
│   └── workflows/
│       └── deploy.yml      # CI/CD pipeline for VPS deployment
├── app.py                  # Flask application and chat API
├── index.html              # Frontend chat interface
├── requirements.txt        # Python dependencies
└── README.md
```

---

## How It Works

1. The resume text is stored in the `RESUME_CONTEXT` variable inside `app.py`.
2. A system prompt instructs the model to answer only from that resume and to decline anything else.
3. The frontend sends the visitor's message to `POST /api/chat`.
4. The backend forwards the system prompt and the message to the OpenRouter API.
5. The model's reply is returned to the frontend and displayed in the chat window.

---

## Getting Started

### Prerequisites

- Python 3.9 or later
- An OpenRouter API key (create one at https://openrouter.ai)
- Git

### Installation

```bash
git clone https://github.com/<your-username>/Personal-resume-chatbot.git
cd Personal-resume-chatbot

python -m venv venv
```

Activate the virtual environment:

```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux / macOS / Git Bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Set the API key

```bash
# Windows (Command Prompt)
set OPENROUTER_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:OPENROUTER_API_KEY="your_api_key_here"

# Linux / macOS / Git Bash
export OPENROUTER_API_KEY=your_api_key_here
```

### Run the application

```bash
python app.py
```

Open http://localhost:5000 in your browser.

---

## Configuration

| Variable | Required | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | Yes | API key used to authenticate requests to OpenRouter |
| `PORT` | No | Port for the development server (default: `5000`) |

The model name, temperature (`0.3`), and token limit (`500`) can be changed in the request payload inside `app.py`.

---

## API Reference

### `GET /`

Serves the chat interface (`index.html`).

### `POST /api/chat`

Sends a message to the assistant and returns its reply.

**Request body**

```json
{
  "message": "What projects has Abdul worked on?"
}
```

**Success response (200)**

```json
{
  "reply": "..."
}
```

**Error responses**

| Status | Meaning |
|---|---|
| `400` | The `message` field is missing or empty |
| `502` | The upstream AI service returned an error |
| `500` | Unexpected server error |

**Example request**

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What are your technical skills?\"}"
```

---

## Deployment

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that deploys the application to an Ubuntu VPS whenever code is pushed to the `main` branch. It can also be triggered manually from the Actions tab.

### What the workflow does

1. Connects to the server over SSH
2. Installs Python, pip, venv, and Nginx
3. Uploads `app.py`, `index.html`, and `requirements.txt` to `/var/www/flaskapp`
4. Writes the API key to a `.env` file on the server
5. Creates a virtual environment and installs dependencies
6. Registers and restarts a Gunicorn systemd service
7. Configures Nginx to serve the frontend and proxy `/api/` requests to Gunicorn

### Required repository secrets

Add these under **Settings > Secrets and variables > Actions**:

| Secret | Description |
|---|---|
| `VPS_HOST` | IP address or hostname of the server |
| `VPS_USERNAME` | SSH username |
| `VPS_PASSWORD` | SSH password |
| `OPENROUTER_API_KEY` | OpenRouter API key |

### Domain

Update the `server_name` value in the Nginx section of `deploy.yml` to match your own domain or subdomain before deploying.

---

## Customization

To adapt the chatbot to a different resume:

1. Open `app.py` and replace the text inside `RESUME_CONTEXT` with the new resume content.
2. Update the assistant name and person's name in `SYSTEM_PROMPT`.
3. Update the page title, heading, and welcome message in `index.html`.

Keep the resume text factual and complete. The assistant can only answer using the information it is given.

---

## Limitations

- Each message is handled independently, so the assistant does not retain conversation history.
- Responses are limited to 500 tokens.
- Answer quality depends on the completeness of the resume text.
- Availability depends on the OpenRouter service and the selected model.

---

## Security Notes

- Never commit your API key or `.env` file. The `.gitignore` file excludes `.env` by default.
- The Flask development server (`python app.py`) is intended for local use only. Production traffic is served through Gunicorn behind Nginx.
- Run the application with `debug=False` in production.
- The CORS policy currently allows all origins. Restrict `Access-Control-Allow-Origin` to your own domain if the API should not be publicly embeddable.
- Prefer SSH key authentication over password authentication for the deployment server.


- GitHub: https://github.com/<your-username>
- LinkedIn: https://www.linkedin.com/in/<your-profile>
- Email: your-email@example.com
