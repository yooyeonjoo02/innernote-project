from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.diary.models import Diary
from app.diary.repository import DiaryRepository
from app.diary.schemas import DiaryCreateRequest, DiaryUpdateRequest
from app.user.models import User


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

        return self.diary_repository.save(db, diary)

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

        if request.content is not None:
            diary.content = request.content

        if request.emotion is not None:
            diary.emotion = request.emotion

        return self.diary_repository.update(db, diary)

    def delete_my_diary(self, db: Session, diary_id: int, current_user: User):
        diary = self.get_my_diary(db, diary_id, current_user)

        diary.is_deleted = True

        return self.diary_repository.update(db, diary)