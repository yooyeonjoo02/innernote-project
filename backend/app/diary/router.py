from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.diary.schemas import (
    DiaryCreateRequest,
    DiaryCreateResponse,
    DiaryResponse,
    DiaryUpdateRequest,
    DiaryUpdateResponse,
    DiaryDeleteResponse
)
from app.diary.service import DiaryService
from app.user.models import User


router = APIRouter(
    prefix="/api/diaries",
    tags=["Diary"]
)

diary_service = DiaryService()


@router.post("", response_model=DiaryCreateResponse)
def create_diary(
    request: DiaryCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    diary = diary_service.create_diary(db, request, current_user)

    return {
        "message": "일기 작성 성공",
        "diary": diary
    }


@router.get("", response_model=list[DiaryResponse])
def get_my_diaries(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return diary_service.get_my_diaries(db, current_user)


@router.get("/{diary_id}", response_model=DiaryResponse)
def get_my_diary(
    diary_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return diary_service.get_my_diary(db, diary_id, current_user)


@router.patch("/{diary_id}", response_model=DiaryUpdateResponse)
def update_my_diary(
    diary_id: int,
    request: DiaryUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    diary = diary_service.update_my_diary(
        db,
        diary_id,
        request,
        current_user
    )

    return {
        "message": "일기 수정 성공",
        "diary": diary
    }


@router.delete("/{diary_id}", response_model=DiaryDeleteResponse)
def delete_my_diary(
    diary_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    diary_service.delete_my_diary(db, diary_id, current_user)

    return {
        "message": "일기 삭제 성공"
    }