from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class EmotionAnalysis(Base):
    __tablename__ = "emotion_analysis"

    id = Column(Integer, primary_key=True, index=True)

    diary_id = Column(
        Integer,
        ForeignKey("diaries.id"),
        nullable=False,
        unique=True
    )

    fear = Column(Float, default=0.0)
    surprise = Column(Float, default=0.0)
    anger = Column(Float, default=0.0)
    sadness = Column(Float, default=0.0)
    neutral = Column(Float, default=0.0)
    happiness = Column(Float, default=0.0)
    disgust = Column(Float, default=0.0)

    dominant_emotion = Column(String(50), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    diary = relationship(
        "Diary",
        back_populates="emotion_analysis"
    )