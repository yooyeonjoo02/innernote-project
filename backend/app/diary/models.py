from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey, DateTime, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, date

from app.database import Base


class Diary(Base):
    __tablename__ = "diaries"

    __table_args__ = (
        UniqueConstraint("user_id", "diary_date", name="uq_user_diary_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    emotion = Column(String(30), nullable=True)
    is_deleted = Column(Boolean, default=False)

    diary_date = Column(Date, nullable=False, default=date.today)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ===== [추천 고정용 캐싱 컬럼 모음] =====
    recommended_music_title = Column(String(255), nullable=True)
    recommended_music_url = Column(String(255), nullable=True)
    
    recommended_place_name = Column(String(255), nullable=True)
    recommended_place_address = Column(String(255), nullable=True)
    recommended_place_url = Column(String(255), nullable=True)

    recommended_mission_title = Column(String(255), nullable=True)
    recommended_mission_description = Column(String(500), nullable=True)
    # ========================================

    user = relationship("User")

    emotion_analysis = relationship(
        "EmotionAnalysis",
        back_populates="diary",
        uselist=False,
        cascade="all, delete-orphan"
    )