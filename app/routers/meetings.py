from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import crud
from app.schemas.meeting import MeetingOut, MeetingDetailOut
from app.services.file_parser import extract_text_from_upload
from app.llm_service import generate_meeting_minutes, LLMGenerationError

router = APIRouter(prefix="/api/meetings", tags=["Meetings"])


@router.post("", response_model=MeetingOut, status_code=201)
async def create_meeting(
    title: str = Form(...),
    raw_text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    if not raw_text and not file:
        raise HTTPException(status_code=400, detail="Provide either raw_text or a file upload.")

    if file:
        raw_bytes = await file.read()
        transcript = extract_text_from_upload(file, raw_bytes)
    else:
        transcript = raw_text

    if not transcript or not transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript is empty.")

    meeting = crud.create_meeting(db, title=title, raw_transcript=transcript)
    return meeting


@router.post("/{meeting_id}/generate", response_model=MeetingDetailOut)
def generate_minutes(meeting_id: int, db: Session = Depends(get_db)):
    meeting = crud.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found.")

    try:
        llm_result = generate_meeting_minutes(meeting.raw_transcript)
    except LLMGenerationError as e:
        crud.update_meeting_status(db, meeting_id, "failed")
        raise HTTPException(status_code=502, detail=f"LLM generation failed: {e}")

    crud.save_meeting_minutes(db, meeting_id, llm_result)
    return crud.get_meeting_detail(db, meeting_id)


@router.get("", response_model=list[MeetingOut])
def list_meetings(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_meetings(db, skip=skip, limit=limit)


@router.get("/{meeting_id}", response_model=MeetingDetailOut)
def get_meeting_detail(meeting_id: int, db: Session = Depends(get_db)):
    detail = crud.get_meeting_detail(db, meeting_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Meeting not found.")
    return detail


@router.delete("/{meeting_id}", status_code=204)
def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_meeting(db, meeting_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Meeting not found.")