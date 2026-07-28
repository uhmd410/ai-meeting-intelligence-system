import json
from sqlalchemy.orm import Session
from app.models.meeting import Meeting, MeetingMinutes, ActionItem


def create_meeting(db: Session, title: str, raw_transcript: str) -> Meeting:
    meeting = Meeting(title=title, raw_transcript=raw_transcript, status="pending")
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting


def get_meeting(db: Session, meeting_id: int) -> Meeting | None:
    return db.query(Meeting).filter(Meeting.id == meeting_id).first()


def get_meetings(db: Session, skip: int = 0, limit: int = 20):
    return (
        db.query(Meeting)
        .order_by(Meeting.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_meeting(db: Session, meeting_id: int) -> bool:
    meeting = get_meeting(db, meeting_id)
    if not meeting:
        return False
    db.delete(meeting)  # cascade handles minutes + action_items
    db.commit()
    return True


def update_meeting_status(db: Session, meeting_id: int, status: str):
    meeting = get_meeting(db, meeting_id)
    if meeting:
        meeting.status = status
        db.commit()


def save_meeting_minutes(db: Session, meeting_id: int, llm_result: dict) -> MeetingMinutes:
    """
    Saves the 5 text-based sections as JSON strings on MeetingMinutes,
    and inserts each action item as its own ActionItem row.
    """
    minutes = MeetingMinutes(
        meeting_id=meeting_id,
        summary=llm_result.get("summary", ""),
        discussion_points=json.dumps(llm_result.get("discussion_points", [])),
        decisions=json.dumps(llm_result.get("decisions", [])),
        risks=json.dumps(llm_result.get("risks", [])),
        next_steps=json.dumps(llm_result.get("next_steps", [])),
    )
    db.add(minutes)

    for item in llm_result.get("action_items", []):
        db.add(ActionItem(
            meeting_id=meeting_id,
            task=item.get("task", ""),
            owner=item.get("owner", "Unassigned"),
            due_date=item.get("due_date", "Not specified"),
            status="open",
        ))

    update_meeting_status(db, meeting_id, "completed")
    db.commit()
    db.refresh(minutes)
    return minutes


def get_meeting_detail(db: Session, meeting_id: int) -> dict | None:
    """
    Builds the full response dict, converting stored JSON strings back
    into real lists for the API response.
    """
    meeting = get_meeting(db, meeting_id)
    if not meeting:
        return None

    minutes_data = None
    if meeting.minutes:
        m = meeting.minutes
        minutes_data = {
            "summary": m.summary,
            "discussion_points": json.loads(m.discussion_points or "[]"),
            "decisions": json.loads(m.decisions or "[]"),
            "risks": json.loads(m.risks or "[]"),
            "next_steps": json.loads(m.next_steps or "[]"),
            "generated_at": m.generated_at,
        }

    action_items_data = [
        {"id": ai.id, "task": ai.task, "owner": ai.owner, "due_date": ai.due_date, "status": ai.status}
        for ai in meeting.action_items
    ]

    return {
        "id": meeting.id,
        "title": meeting.title,
        "status": meeting.status,
        "created_at": meeting.created_at,
        "raw_transcript": meeting.raw_transcript,
        "minutes": minutes_data,
        "action_items": action_items_data,
    }