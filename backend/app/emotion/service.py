from sqlalchemy.orm import Session

from app.emotion.models import EmotionAnalysis
from app.emotion.repository import EmotionRepository
from app.emotion.schemas import EmotionCreateRequestDTO


class EmotionService:

    @staticmethod
    def create_emotion(
        db: Session,
        request: EmotionCreateRequestDTO
    ):

        emotion = EmotionAnalysis(
            diary_id=request.diary_id,

            fear=request.fear,
            surprise=request.surprise,
            anger=request.anger,
            sadness=request.sadness,
            neutral=request.neutral,
            happiness=request.happiness,
            disgust=request.disgust,

            dominant_emotion=request.dominant_emotion
        )

        return EmotionRepository.create(db, emotion)

    @staticmethod
    def get_emotion(
        db: Session,
        emotion_id: int
    ):

        return EmotionRepository.find_by_id(db, emotion_id)

    @staticmethod
    def get_by_diary(
        db: Session,
        diary_id: int
    ):

        return EmotionRepository.find_by_diary_id(db, diary_id)

    @staticmethod
    def delete_emotion(
        db: Session,
        emotion_id: int
    ):

        emotion = EmotionRepository.find_by_id(db, emotion_id)

        if not emotion:
            return None

        EmotionRepository.delete(db, emotion)

        return True