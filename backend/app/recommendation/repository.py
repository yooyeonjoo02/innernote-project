from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
from datetime import date, timedelta

from app.diary.models import Diary
from app.emotion.models import EmotionAnalysis
from app.survey.models import Survey


class RecommendationRepository:

    @staticmethod
    def find_diary_by_user_and_date(
        db: Session,
        user_id: int,
        target_date: date
    ):
        return db.query(Diary).filter(
            Diary.user_id == user_id,
            cast(Diary.diary_date + timedelta(hours=9), Date) == target_date,
            Diary.is_deleted == False
        ).order_by(Diary.diary_date.desc()).first()

    @staticmethod
    def find_emotion_by_diary_id(db: Session, diary_id: int):
        return db.query(EmotionAnalysis).filter(
            EmotionAnalysis.diary_id == diary_id
        ).first()

    @staticmethod
    def find_survey_by_user_id(db: Session, user_id: int):
        return db.query(Survey).filter(
            Survey.user_id == user_id
        ).first()