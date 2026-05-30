from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

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
        existing_diary = self.diary_repository.find_by_date_and_user_id(
            db,
            request.diary_date,
            current_user.id
        )

        if existing_diary is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="해당 날짜에 이미 작성된 일기가 있습니다."
            )

        analyzed_emotion = analyze_emotion_for_db(request.content)

        diary = Diary(
            content=request.content,
            emotion=analyzed_emotion["dominant_emotion"],
            diary_date=request.diary_date,
            user_id=current_user.id
        )

        self.diary_repository.save(db, diary)

        emotion_analysis = EmotionAnalysis(
            diary_id=diary.id,
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
        db.refresh(diary)

        return diary

    def get_my_diaries(self, db: Session, current_user: User):
        return self.diary_repository.find_all_by_user_id(db, current_user.id)

    def get_diary_by_date(
        self,
        db: Session,
        diary_date: date,
        current_user: User
    ):
        diary = self.diary_repository.find_by_date_and_user_id(
            db,
            diary_date,
            current_user.id
        )

        if diary is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 날짜의 일기를 찾을 수 없습니다."
            )

        return diary

    def get_diary_dates(self, db: Session, current_user: User):
        dates = self.diary_repository.find_dates_by_user_id(
            db,
            current_user.id
        )

        return [item.diary_date for item in dates]

    def update_diary_by_date(
        self,
        db: Session,
        diary_date: date,
        request: DiaryUpdateRequest,
        current_user: User
    ):
        diary = self.diary_repository.find_by_date_and_user_id(
            db,
            diary_date,
            current_user.id
        )

        if diary is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 날짜의 일기를 찾을 수 없습니다."
            )

        analyzed_emotion = analyze_emotion_for_db(request.content)

        diary.content = request.content
        diary.emotion = analyzed_emotion["dominant_emotion"]

        emotion_analysis = db.query(EmotionAnalysis).filter(
            EmotionAnalysis.diary_id == diary.id
        ).first()

        if emotion_analysis is None:
            emotion_analysis = EmotionAnalysis(
                diary_id=diary.id
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
        db.refresh(diary)

        return diary