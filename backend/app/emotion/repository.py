from sqlalchemy.orm import Session

from app.emotion.models import EmotionAnalysis


class EmotionRepository:

    @staticmethod
    def save(db: Session, emotion: EmotionAnalysis):
        db.add(emotion)
        db.flush()
        return emotion

    @staticmethod
    def find_by_diary_id(db: Session, diary_id: int):
        return db.query(EmotionAnalysis).filter(
            EmotionAnalysis.diary_id == diary_id
        ).first()