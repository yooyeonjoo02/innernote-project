from sqlalchemy.orm import Session

from app.emotion.repository import EmotionRepository


class EmotionService:

    @staticmethod
    def get_by_diary(
        db: Session,
        diary_id: int
    ):

        return EmotionRepository.find_by_diary_id(db, diary_id)