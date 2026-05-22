from sqlalchemy.orm import Session

from app.emotion.models import EmotionAnalysis


class EmotionRepository:

    @staticmethod
    def create(db: Session, emotion: EmotionAnalysis):
        db.add(emotion)
        db.commit()
        db.refresh(emotion)
        return emotion

    @staticmethod
    def find_by_id(db: Session, emotion_id: int):
        return db.query(EmotionAnalysis).filter(
            EmotionAnalysis.id == emotion_id
        ).first()

    @staticmethod
    def find_by_diary_id(db: Session, diary_id: int):
        return db.query(EmotionAnalysis).filter(
            EmotionAnalysis.diary_id == diary_id
        ).first()

    @staticmethod
    def delete(db: Session, emotion: EmotionAnalysis):
        db.delete(emotion)
        db.commit()