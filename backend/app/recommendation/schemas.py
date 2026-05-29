from pydantic import BaseModel
from typing import Optional


class MusicRecommendation(BaseModel):
    title: str
    url: str


class PlaceRecommendation(BaseModel):
    name: str
    address: Optional[str] = None
    url: Optional[str] = None


class MissionRecommendation(BaseModel):
    title: str
    description: Optional[str] = None


class DailyRecommendationResponse(BaseModel):
    target_date: str
    happiness: float
    recommendation_type: str
    music: MusicRecommendation
    place: PlaceRecommendation
    mission: MissionRecommendation