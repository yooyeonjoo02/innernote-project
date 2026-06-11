from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.diary.models import Diary
from app.emotion.models import EmotionAnalysis
from app.survey.models import Survey

class RecommendationRepository:

    @staticmethod
    def find_diary_by_user_and_date(db: Session, user_id: int, target_date: date):
        return db.query(Diary).filter(
            Diary.user_id == user_id,
            Diary.diary_date == target_date,
            Diary.is_deleted == False
        ).first()

    @staticmethod
    def find_emotion_by_diary_id(db: Session, diary_id: int):
        return db.query(EmotionAnalysis).filter(EmotionAnalysis.diary_id == diary_id).first()

    @staticmethod
    def find_survey_by_user_id(db: Session, user_id: int):
        return db.query(Survey).filter(Survey.user_id == user_id).first()

    @staticmethod
    def find_recent_recommended_places(db: Session, user_id: int, target_date: date, days: int = 21):
        cutoff_date = target_date - timedelta(days=days)
        recent_diaries = db.query(Diary.recommended_place_name).filter(
            Diary.user_id == user_id,
            Diary.diary_date >= cutoff_date,
            Diary.diary_date < target_date,
            Diary.recommended_place_name.isnot(None),
            Diary.is_deleted == False
        ).all()
        return [d[0] for d in recent_diaries]

    # ===== [신규] 최근 10개의 미션 중복 방지용 쿼리 =====
    @staticmethod
    def find_recent_recommended_missions(db: Session, user_id: int, target_date: date, limit: int = 10):
        # 날짜 내림차순(최신순)으로 최근 10개만 가져옴
        recent_diaries = db.query(Diary.recommended_mission_title).filter(
            Diary.user_id == user_id,
            Diary.diary_date < target_date,
            Diary.recommended_mission_title.isnot(None),
            Diary.is_deleted == False
        ).order_by(Diary.diary_date.desc()).limit(limit).all()
        
        return [d[0] for d in recent_diaries]
    # ====================================================

    # ===== [신규] 최근 14일(2주) 음악 중복 방지용 쿼리 =====
    @staticmethod
    def find_recent_recommended_music(db: Session, user_id: int, target_date: date, days: int = 14):
        cutoff_date = target_date - timedelta(days=days)
        recent_diaries = db.query(Diary.recommended_music_title).filter(
            Diary.user_id == user_id,
            Diary.diary_date >= cutoff_date,
            Diary.diary_date < target_date,
            Diary.recommended_music_title.isnot(None),
            Diary.is_deleted == False
        ).all()
        
        return [d[0] for d in recent_diaries]
    # ====================================================