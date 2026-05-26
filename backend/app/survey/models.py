from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    favorite_singer = Column(String(50), nullable=True)
    favorite_genre = Column(String(30), nullable=True)
    residence_area = Column(String(30), nullable=True)
    favorite_place = Column(String(50), nullable=True)
    want_to_go_place = Column(String(50), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
