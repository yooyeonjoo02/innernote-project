from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Diary(Base):
    __tablename__ = "diaries"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    emotion = Column(String(30), nullable=True)
    is_deleted = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User")

    emotion_analysis = relationship(
    "EmotionAnalysis",
    back_populates="diary",
    uselist=False,
    cascade="all, delete-orphan"
)