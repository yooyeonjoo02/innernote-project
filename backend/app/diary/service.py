from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.diary.models import Diary
from app.diary.repository import DiaryRepository
from app.diary.schemas import DiaryCreateRequest, DiaryUpdateRequest
from app.user.models import User

from app.emotion.models import EmotionAnalysis
from app.ai.emotion_analyzer import analyze_emotion_for_db


class DiaryService:

    def __init__(self):
        self.diary_repository = DiaryRepository()

    def create_diary(
        self,
        db: Session,
        request: DiaryCreateRequest,
        current_user: User
    ):
        diary = Diary(
            content=request.content,
            emotion=request.emotion,
            user_id=current_user.id
        )

        saved_diary = self.diary_repository.save(db, diary)

        analyzed_emotion = analyze_emotion_for_db(request.content)

        emotion_analysis = EmotionAnalysis(
            diary_id=saved_diary.id,
            fear=analyzed_emotion["fear"],
            surprise=analyzed_emotion["surprise"],
            anger=analyzed_emotion["anger"],
            sadness=analyzed_emotion["sadness"],
            neutral=analyzed_emotion["neutral"],
            happiness=analyzed_emotion["happiness"],
            disgust=analyzed_emotion["disgust"],
            dominant_emotion=analyzed_emotion["dominant_emotion"]
        )

        db.add(emotion_analysis)
        db.commit()
        db.refresh(saved_diary)

        return saved_diary

    def get_my_diaries(self, db: Session, current_user: User):
        return self.diary_repository.find_all_by_user_id(db, current_user.id)

    def get_my_diary(self, db: Session, diary_id: int, current_user: User):
        diary = self.diary_repository.find_by_id_and_user_id(
            db,
            diary_id,
            current_user.id
        )

        if diary is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="일기를 찾을 수 없습니다."
            )

        return diary

    def update_my_diary(
        self,
        db: Session,
        diary_id: int,
        request: DiaryUpdateRequest,
        current_user: User
    ):
        diary = self.get_my_diary(db, diary_id, current_user)

        is_content_updated = False

        if request.content is not None:
            diary.content = request.content
            is_content_updated = True

        if request.emotion is not None:
            diary.emotion = request.emotion

        updated_diary = self.diary_repository.update(db, diary)

        if is_content_updated:
            analyzed_emotion = analyze_emotion_for_db(updated_diary.content)

            emotion_analysis = db.query(EmotionAnalysis).filter(
                EmotionAnalysis.diary_id == updated_diary.id
            ).first()

            if emotion_analysis is None:
                emotion_analysis = EmotionAnalysis(
                    diary_id=updated_diary.id
                )
                db.add(emotion_analysis)

            emotion_analysis.fear = analyzed_emotion["fear"]
            emotion_analysis.surprise = analyzed_emotion["surprise"]
            emotion_analysis.anger = analyzed_emotion["anger"]
            emotion_analysis.sadness = analyzed_emotion["sadness"]
            emotion_analysis.neutral = analyzed_emotion["neutral"]
            emotion_analysis.happiness = analyzed_emotion["happiness"]
            emotion_analysis.disgust = analyzed_emotion["disgust"]
            emotion_analysis.dominant_emotion = analyzed_emotion["dominant_emotion"]

            db.commit()
            db.refresh(updated_diary)

        return updated_diary

    def delete_my_diary(self, db: Session, diary_id: int, current_user: User):
        diary = self.get_my_diary(db, diary_id, current_user)

        diary.is_deleted = True

        return self.diary_repository.update(db, diary)