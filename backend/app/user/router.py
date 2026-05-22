from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.user.models import User
from app.user.schemas import (
    UserSignupRequest,
    UserSignupResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserMeResponse,
    UserUpdateRequest,
    UserUpdateResponse
)
from app.user.service import UserService
from app.core.security import get_current_user


router = APIRouter(
    prefix="/api/users",
    tags=["User"]
)

user_service = UserService()


@router.post("/signup", response_model=UserSignupResponse)
def signup(
    request: UserSignupRequest,
    db: Session = Depends(get_db)
):
    user = user_service.signup(db, request)

    return {
        "message": "회원가입 성공",
        "user": user
    }


@router.post("/login", response_model=UserLoginResponse)
def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db)
):
    access_token = user_service.login(db, request)

    return {
        "message": "로그인 성공",
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserMeResponse)
def get_my_info(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.patch("/me", response_model=UserUpdateResponse)
def update_my_info(
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = user_service.update_my_info(db, current_user, request)

    return {
        "message": "내 정보 수정 성공",
        "user": user
    }