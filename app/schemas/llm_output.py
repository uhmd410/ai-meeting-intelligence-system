from pydantic import BaseModel
from typing import List

class LLMActionItem(BaseModel):
    task: str
    owner: str = "Unassigned"
    due_date: str = "Not specified"

class LLMMeetingMinutes(BaseModel):
    summary: str
    discussion_points: List[str] = []
    decisions: List[str] = []
    action_items: List[LLMActionItem] = []
    risks: List[str] = []
    next_steps: List[str] = []