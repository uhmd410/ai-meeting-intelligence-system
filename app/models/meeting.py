from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    raw_transcript = Column(Text, nullable=False)
    status = Column(String(20), default="pending", index=True)  # pending | completed | failed
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    minutes = relationship("MeetingMinutes", back_populates="meeting", uselist=False, cascade="all, delete-orphan")
    action_items = relationship("ActionItem", back_populates="meeting", cascade="all, delete-orphan")


class MeetingMinutes(Base):
    __tablename__ = "meeting_minutes"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False, unique=True)

    summary = Column(Text)
    discussion_points = Column(Text)   # JSON string
    decisions = Column(Text)           # JSON string
    risks = Column(Text)               # JSON string
    next_steps = Column(Text)          # JSON string
    generated_at = Column(DateTime, default=datetime.utcnow)

    meeting = relationship("Meeting", back_populates="minutes")


class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False, index=True)

    task = Column(Text, nullable=False)
    owner = Column(String(100), default="Unassigned", index=True)
    due_date = Column(String(50), default="Not specified", index=True)
    status = Column(String(20), default="open", index=True)  # open | done

    meeting = relationship("Meeting", back_populates="action_items")