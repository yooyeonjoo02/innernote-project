from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.core.security import get_current_user
from app.user.models import User
from app.recommendation.service import RecommendationService
from app.recommendation.schemas import DailyRecommendationResponse


router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendation"]
)

recommendation_service = RecommendationService()


@router.get(
    "/daily",
    response_model=DailyRecommendationResponse
)
def get_daily_recommendation(
    target_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return recommendation_service.get_daily_recommendation(
        db=db,
        user_id=current_user.id,
        target_date=target_date
    )