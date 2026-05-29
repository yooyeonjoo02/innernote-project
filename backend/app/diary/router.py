from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.core.security import get_current_user
from app.database import get_db
from app.diary.schemas import (
    DiaryCreateRequest,
    DiaryCreateResponse,
    DiaryResponse,
    DiaryUpdateRequest,
    DiaryUpdateResponse
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


@router.get("/dates")
def get_diary_dates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return diary_service.get_diary_dates(db, current_user)


@router.get("/date/{diary_date}", response_model=DiaryResponse)
def get_diary_by_date(
    diary_date: date,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return diary_service.get_diary_by_date(db, diary_date, current_user)


@router.patch("/date/{diary_date}", response_model=DiaryUpdateResponse)
def update_diary_by_date(
    diary_date: date,
    request: DiaryUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    diary = diary_service.update_diary_by_date(
        db,
        diary_date,
        request,
        current_user
    )

    return {
        "message": "일기 수정 성공",
        "diary": diary
    }