from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SurveyRequest(BaseModel):
    favorite_singer: Optional[str] = None
    favorite_genre: Optional[str] = None
    residence_area: Optional[str] = None
    favorite_place: Optional[str] = None
    want_to_go_place: Optional[str] = None


class SurveyResponse(BaseModel):
    id: int
    user_id: int
    favorite_singer: Optional[str]
    favorite_genre: Optional[str]
    residence_area: Optional[str]
    favorite_place: Optional[str]
    want_to_go_place: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SurveySaveResponse(BaseModel):
    message: str
    survey: SurveyResponse
