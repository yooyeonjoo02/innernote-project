from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.survey.schemas import SurveyRequest, SurveyResponse, SurveySaveResponse
from app.survey.service import SurveyService
from app.user.models import User


router = APIRouter(
    prefix="/api/surveys",
    tags=["Survey"]
)

survey_service = SurveyService()


@router.post("", response_model=SurveySaveResponse)
def save_survey(
    request: SurveyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    survey = survey_service.save_survey(db, request, current_user)

    return {
        "message": "설문 저장 성공",
        "survey": survey
    }


@router.get("/me", response_model=SurveyResponse)
def get_my_survey(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return survey_service.get_my_survey(db, current_user)
