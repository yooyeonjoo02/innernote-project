from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.survey.models import Survey
from app.survey.repository import SurveyRepository
from app.survey.schemas import SurveyRequest
from app.user.models import User


class SurveyService:

    def __init__(self):
        self.survey_repository = SurveyRepository()

    def save_survey(self, db: Session, request: SurveyRequest, current_user: User):
        survey = self.survey_repository.find_by_user_id(db, current_user.id)

        if survey:
            survey.favorite_singer = request.favorite_singer
            survey.favorite_genre = request.favorite_genre
            survey.residence_area = request.residence_area
            survey.favorite_place = request.favorite_place
            survey.want_to_go_place = request.want_to_go_place
            return self.survey_repository.update(db, survey)

        survey = Survey(
            user_id=current_user.id,
            favorite_singer=request.favorite_singer,
            favorite_genre=request.favorite_genre,
            residence_area=request.residence_area,
            favorite_place=request.favorite_place,
            want_to_go_place=request.want_to_go_place
        )
        return self.survey_repository.save(db, survey)

    def get_my_survey(self, db: Session, current_user: User):
        survey = self.survey_repository.find_by_user_id(db, current_user.id)

        if not survey:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="설문 데이터가 없습니다."
            )

        return survey
