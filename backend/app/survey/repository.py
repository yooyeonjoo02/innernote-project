from sqlalchemy.orm import Session

from app.survey.models import Survey


class SurveyRepository:

    def find_by_user_id(self, db: Session, user_id: int):
        return db.query(Survey).filter(Survey.user_id == user_id).first()

    def save(self, db: Session, survey: Survey):
        db.add(survey)
        db.commit()
        db.refresh(survey)
        return survey

    def update(self, db: Session, survey: Survey):
        db.commit()
        db.refresh(survey)
        return survey
