# AI Meeting Intelligence System

AI-powered web application that converts meeting transcripts into structured
meeting minutes using an LLM (Groq), with action item tracking, PDF/DOCX
export, and audio transcription support.

## Features

- Create meetings by pasting text, uploading a transcript file (.txt/.docx),
  or uploading an audio recording (.mp3/.wav/.m4a/.ogg) — audio is
  transcribed via Groq Whisper before processing
- AI-generated Summary, Discussion Points, Decisions, Action Items (with
  owner/due date), Risks, and Next Steps
- Meeting history with search, sort, and pagination
- PDF and DOCX export of generated minutes
- Light/dark theme toggle
- REST API with full Swagger/OpenAPI documentation

## Tech Stack

Python, FastAPI, Groq API (LLM + Whisper transcription), SQLAlchemy, SQLite,
Jinja2Templates, HTML/CSS/Bootstrap 5, vanilla JavaScript, python-docx,
fpdf2

## Project Structure

```
ai-meeting-intelligence-system/
├── app/
│   ├── models/              # SQLAlchemy models (Meeting, MeetingMinutes, ActionItem)
│   ├── prompts/             # LLM prompt templates
│   ├── routers/             # API and page routes
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # file_parser, audio_service, and other service logic
│   ├── static/              # CSS and JS assets
│   │   ├── css/
│   │   └── js/
│   ├── templates/           # Jinja2-served HTML pages
│   ├── __init__.py
│   ├── crud.py              # Database access layer
│   ├── database.py          # SQLAlchemy engine/session config
│   ├── export_service.py    # PDF/DOCX export generation
│   ├── llm_service.py       # Groq LLM integration
│   └── main.py              # App entrypoint, router/static/template setup
├── samples/                 # Sample transcripts + captured LLM outputs
├── screenshots/
├── scripts/                 # Dev/test utility scripts
├── tests/                   # Pytest test suite
│   ├── test_meetings.py
│   └── test_pages.py
├── .env                     # Local secrets (not committed)
├── .env.example             # Template for required environment variables
├── .gitignore
├── meetings.db              # SQLite database (generated on first run)
├── README.md
└── requirements.txt
```

## Setup & Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/uhmd410/ai-meeting-intelligence-system.git
   cd ai-meeting-intelligence-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate   # Git Bash on Windows
   # or venv\Scripts\activate     # CMD/PowerShell
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables — copy `.env.example` to `.env` and fill in:
   ```
   GROQ_API_KEY=your_key_here
   DATABASE_URL=sqlite:///./meetings.db
   ```

5. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Open:
   - Web app: http://127.0.0.1:8000/
   - API docs (Swagger): http://127.0.0.1:8000/docs

## API Overview

Full interactive documentation is available at `/docs`. Core endpoints:

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/meetings` | Create a meeting from pasted text, a `.txt`/`.docx` file, or an audio file |
| POST | `/api/meetings/{id}/generate` | Run LLM processing to generate structured minutes |
| GET | `/api/meetings` | List meeting history (paginated) |
| GET | `/api/meetings/{id}` | Full meeting detail, including minutes and action items |
| DELETE | `/api/meetings/{id}` | Delete a meeting and its associated minutes/action items |
| GET | `/api/meetings/{id}/export/pdf` | Download generated minutes as PDF |
| GET | `/api/meetings/{id}/export/docx` | Download generated minutes as DOCX |

## Prompt Engineering Approach

Meeting minutes are generated using a system prompt that requires strict
JSON output across six fields (summary, discussion points, decisions,
action items, risks, next steps), with explicit instructions against
fabricating content for empty sections. If the LLM returns malformed JSON
or invalid structure, the service automatically retries once with a
corrective follow-up message before raising an error. This was validated
against three deliberately varied sample transcripts (formal, informal,
and very short) — see `/samples`.

## Screenshots

See `/screenshots` for: Dashboard, New Meeting (text/file/audio upload),
Meeting Detail, History, Dark Mode.

## Sample Data

See `/samples` for example transcripts (formal, informal, short) and their
generated outputs, used to validate prompt reliability during development.

## Stretch Goals Implemented

- **Audio Upload** — meetings can be created directly from audio recordings
  (`.mp3`, `.wav`, `.m4a`, `.ogg`); audio is transcribed via Groq's Whisper
  API before being passed through the same LLM pipeline used for text
  transcripts.
- **Dark Mode** — light/dark theme toggle available from the navigation
  header, with the preference persisted across sessions.
