from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.user.models import User
from app.user.repository import UserRepository
from app.user.schemas import UserSignupRequest, UserLoginRequest


class UserService:

    def __init__(self):
        self.user_repository = UserRepository()

    def signup(self, db: Session, request: UserSignupRequest):
        existing_user = self.user_repository.find_by_email(db, request.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 이메일입니다."
            )

        user = User(
            email=request.email,
            password=hash_password(request.password),
            nickname=request.nickname
        )

        return self.user_repository.save(db, user)

    def login(self, db: Session, request: UserLoginRequest):
        user = self.user_repository.find_by_email(db, request.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다."
            )

        if not verify_password(request.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다."
            )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email
            }
        )

        return access_token