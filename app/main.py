import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app import models
from app.routers import meetings, pages

app = FastAPI(
    title="AI Meeting Intelligence System",
    description="Converts meeting transcripts into structured Meeting Minutes using an LLM.",
    version="1.0.0",
)

# CORS — allow the frontend (served on any port/origin during development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# JSON API routes (prefixed with /api)
app.include_router(meetings.router)

# HTML page routes (served via Jinja2Templates)
app.include_router(pages.router)

# Serve static assets (CSS, JS) at /static
_static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=_static_dir), name="static")

@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "AI Meeting Intelligence System"}

