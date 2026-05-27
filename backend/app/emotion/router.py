from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.emotion.schemas import (
    EmotionCreateRequestDTO,
    EmotionResponseDTO
)

from app.emotion.service import EmotionService

router = APIRouter(
    prefix="/api/emotions",
    tags=["Emotion"]
)


@router.post(
    "",
    response_model=EmotionResponseDTO
)
def create_emotion(
    request: EmotionCreateRequestDTO,
    db: Session = Depends(get_db)
):

    return EmotionService.create_emotion(db, request)


@router.get(
    "/{emotion_id}",
    response_model=EmotionResponseDTO
)
def get_emotion(
    emotion_id: int,
    db: Session = Depends(get_db)
):

    emotion = EmotionService.get_emotion(
        db,
        emotion_id
    )

    if not emotion:
        raise HTTPException(
            status_code=404,
            detail="Emotion not found"
        )

    return emotion


@router.get(
    "/diary/{diary_id}",
    response_model=EmotionResponseDTO
)
def get_emotion_by_diary(
    diary_id: int,
    db: Session = Depends(get_db)
):

    emotion = EmotionService.get_by_diary(
        db,
        diary_id
    )

    if not emotion:
        raise HTTPException(
            status_code=404,
            detail="Emotion not found"
        )

    return emotion


@router.delete("/{emotion_id}")
def delete_emotion(
    emotion_id: int,
    db: Session = Depends(get_db)
):

    result = EmotionService.delete_emotion(
        db,
        emotion_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Emotion not found"
        )

    return {
        "message": "Emotion deleted successfully"
    }