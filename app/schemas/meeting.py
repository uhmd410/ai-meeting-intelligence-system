from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class ActionItemCreate(BaseModel):
    task: str
    owner: str = "Unassigned"
    due_date: str = "Not specified"

class ActionItemOut(ActionItemCreate):
    id: int
    status: str = "open"

    model_config = ConfigDict(from_attributes=True)

class MeetingCreate(BaseModel):
    title: str
    raw_transcript: str

class MeetingMinutesOut(BaseModel):
    summary: Optional[str] = None
    discussion_points: List[str] = []
    decisions: List[str] = []
    risks: List[str] = []
    next_steps: List[str] = []
    generated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class MeetingOut(BaseModel):
    id: int
    title: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MeetingDetailOut(MeetingOut):
    raw_transcript: str
    minutes: Optional[MeetingMinutesOut] = None
    action_items: List[ActionItemOut] = []