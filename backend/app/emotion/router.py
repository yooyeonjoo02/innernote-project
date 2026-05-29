from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.emotion.schemas import EmotionResponseDTO
from app.emotion.service import EmotionService


router = APIRouter(
    prefix="/api/emotions",
    tags=["Emotion"]
)


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