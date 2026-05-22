from datetime import datetime
from pydantic import BaseModel, Field


class DiaryCreateRequest(BaseModel):
    content: str = Field(min_length=1)
    emotion: str | None = None


class DiaryUpdateRequest(BaseModel):
    content: str | None = Field(default=None, min_length=1)
    emotion: str | None = None


class DiaryResponse(BaseModel):
    id: int
    content: str
    emotion: str | None
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


class DiaryDeleteResponse(BaseModel):
    message: str