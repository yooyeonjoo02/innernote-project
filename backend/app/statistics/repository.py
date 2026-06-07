from sqlalchemy.orm import Session
from datetime import date
from app.diary.models import Diary
from app.emotion.models import EmotionAnalysis

class StatisticsRepository:

    @staticmethod
    def find_diary_by_date(db: Session, user_id: int, target_date: date):
        """특정 날짜의 유저 일기를 가져옵니다."""
        return db.query(Diary).filter(
            Diary.user_id == user_id,          # [핵심 수정] 타 유저 데이터 혼입 방지
            Diary.diary_date == target_date,
            Diary.is_deleted == False
        ).first()

    @staticmethod
    def find_diaries_with_emotion_analysis(db: Session, user_id: int, start_date: date, end_date: date):
        """특정 기간 동안의 유저 일기와 감정 분석 결과를 함께 가져옵니다."""
        return db.query(Diary, EmotionAnalysis).join(
            EmotionAnalysis, Diary.id == EmotionAnalysis.diary_id
        ).filter(
            Diary.user_id == user_id,          # [핵심 수정] 타 유저 데이터 혼입 방지
            Diary.diary_date >= start_date,
            Diary.diary_date <= end_date,
            Diary.is_deleted == False
        ).order_by(Diary.diary_date.asc()).all()