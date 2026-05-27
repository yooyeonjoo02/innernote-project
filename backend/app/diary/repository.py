from sqlalchemy.orm import Session

from app.diary.models import Diary


class DiaryRepository:

    def save(self, db: Session, diary: Diary):
        db.add(diary)
        db.commit()
        db.refresh(diary)
        return diary

    def find_all_by_user_id(self, db: Session, user_id: int):
        return db.query(Diary).filter(
            Diary.user_id == user_id,
            Diary.is_deleted == False
        ).order_by(Diary.created_at.desc()).all()

    def find_by_id_and_user_id(self, db: Session, diary_id: int, user_id: int):
        return db.query(Diary).filter(
            Diary.id == diary_id,
            Diary.user_id == user_id,
            Diary.is_deleted == False
        ).first()

    def update(self, db: Session, diary: Diary):
        db.commit()
        db.refresh(diary)
        return diary