from datetime import datetime, date
from pydantic import BaseModel, Field


class DiaryCreateRequest(BaseModel):
    content: str = Field(min_length=1)
    diary_date: date


class DiaryUpdateRequest(BaseModel):
    content: str = Field(min_length=1)


class DiaryResponse(BaseModel):
    id: int
    content: str
    emotion: str | None
    diary_date: date
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DiaryCreateResponse(BaseModel):
    message: str
    diary: DiaryResponse


class DiaryUpdateResponse(BaseModel):
    message: str
    diary: DiaryResponse