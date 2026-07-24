# app/main.py
from fastapi import FastAPI
from app.database import Base, engine
from app import models

app = FastAPI(
    title="AI Meeting Intelligence System",
    description="Converts meeting transcripts into structured Meeting Minutes using an LLM.",
    version="1.0.0",
)

# Create tables on startup (fine for SQLite/dev; you'd use Alembic migrations in production)
Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "AI Meeting Intelligence System"}