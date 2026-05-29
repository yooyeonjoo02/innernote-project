from sqlalchemy.orm import Session

from app.diary.models import Diary


class DiaryRepository:

    def save(self, db: Session, diary: Diary):
        db.add(diary)
        db.flush()
        return diary

    def find_all_by_user_id(self, db: Session, user_id: int):
        return db.query(Diary).filter(
            Diary.user_id == user_id,
            Diary.is_deleted == False
        ).order_by(Diary.diary_date.desc()).all()

    def find_by_id_and_user_id(self, db: Session, diary_id: int, user_id: int):
        return db.query(Diary).filter(
            Diary.id == diary_id,
            Diary.user_id == user_id,
            Diary.is_deleted == False
        ).first()

    def find_by_date_and_user_id(self, db: Session, diary_date, user_id: int):
        return db.query(Diary).filter(
            Diary.diary_date == diary_date,
            Diary.user_id == user_id,
            Diary.is_deleted == False
        ).first()

    def find_dates_by_user_id(self, db: Session, user_id: int):
        return db.query(Diary.diary_date).filter(
            Diary.user_id == user_id,
            Diary.is_deleted == False
        ).order_by(Diary.diary_date.desc()).all()

    def update(self, db: Session, diary: Diary):
        db.flush()
        return diary