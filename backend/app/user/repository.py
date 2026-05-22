from sqlalchemy.orm import Session

from app.user.models import User


class UserRepository:

    def find_by_email(self, db: Session, email: str):
        return db.query(User).filter(
            User.email == email,
            User.is_deleted == False
        ).first()

    def save(self, db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user