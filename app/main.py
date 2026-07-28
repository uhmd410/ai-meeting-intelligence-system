from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import meetings

app = FastAPI(
    title="AI Meeting Intelligence System",
    description="Converts meeting transcripts into structured Meeting Minutes using an LLM.",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(meetings.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "AI Meeting Intelligence System"}
