from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.user.models import User
from app.user.repository import UserRepository
from app.user.schemas import (
    UserSignupRequest,
    UserLoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest
)


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
                "sub": user.email
            }
        )

        return access_token

    def update_my_info(self, db: Session, current_user: User, request):
        current_user.update_nickname(request.nickname)

        return self.user_repository.update(db, current_user)

    def delete_my_account(self, db: Session, current_user: User):
        current_user.delete()

        return self.user_repository.update(db, current_user)

    def forgot_password(self, db: Session, request: ForgotPasswordRequest):
        user = self.user_repository.find_by_email(db, request.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 이메일입니다."
            )

        return {
            "message": "비밀번호 재설정 요청 성공",
            "reset_token": user.email
        }

    def reset_password(self, db: Session, request: ResetPasswordRequest):
        user = self.user_repository.find_by_email(db, request.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 이메일입니다."
            )

        user.password = hash_password(request.new_password)

        self.user_repository.update(db, user)

        return {
            "message": "비밀번호 변경 성공"
        }