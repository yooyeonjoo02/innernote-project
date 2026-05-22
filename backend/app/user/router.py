from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.user.schemas import (
    UserSignupRequest,
    UserSignupResponse,
    UserLoginRequest,
    UserLoginResponse
)
from app.user.service import UserService


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