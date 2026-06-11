from sqlalchemy.orm import Session
from datetime import date

from app.diary.models import Diary
from app.emotion.models import EmotionAnalysis
from app.survey.models import Survey


class StatisticsRepository:

    @staticmethod
    def find_diary_by_date(db: Session, user_id: int, target_date: date):
        return db.query(Diary).filter(
            Diary.user_id == user_id,  # [수정] 타 유저 데이터 혼입 방지
            Diary.diary_date == target_date,
            Diary.is_deleted == False
        ).order_by(Diary.diary_date.desc()).first()

    @staticmethod
    def find_emotion_analysis_by_diary_id(db: Session, diary_id: int):
        return db.query(EmotionAnalysis).filter(
            EmotionAnalysis.diary_id == diary_id
        ).first()

    @staticmethod
    def find_survey_by_user_id(db: Session, user_id: int):
        return db.query(Survey).filter(
            Survey.user_id == user_id
        ).first()

    @staticmethod
    def find_diaries_with_emotion_analysis(
        db: Session,
        user_id: int,
        start_date: date,
        end_date: date
    ):
        return db.query(Diary).join(
            EmotionAnalysis,
            Diary.id == EmotionAnalysis.diary_id
        ).filter(
            Diary.user_id == user_id,  # [수정] 타 유저 데이터 혼입 방지
            Diary.diary_date >= start_date,
            Diary.diary_date <= end_date,
            Diary.is_deleted == False
        ).order_by(Diary.diary_date.asc()).all()