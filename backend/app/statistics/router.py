from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.statistics.service import StatisticsService
# [추가] 로그인한 현재 유저 정보를 가져오는 함수 import (프로젝트 경로에 맞게 수정 필요 시 수정)
from app.core.security import get_current_user


router = APIRouter(
    prefix="/api/v1/statistics",
    tags=["statistics"]
)


@router.get("/daily")
async def get_daily_statistics(
    date: str = Query(..., description="조회 대상 일자 (YYYY-MM-DD 포맷)"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # [추가] 현재 유저 가져오기
):
    # [수정] current_user.id 전달
    return StatisticsService.get_daily_statistics(db, current_user.id, date)


@router.get("/weekly")
async def get_weekly_statistics(
    date: str = Query(..., description="조회 기준 일자 (YYYY-MM-DD 포맷)"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # [추가] 현재 유저 가져오기
):
    # [수정] current_user.id 전달
    return StatisticsService.get_weekly_statistics(db, current_user.id, date)


@router.get("/monthly")
async def get_monthly_statistics(
    date: str = Query(..., description="조회 기준 일자 (YYYY-MM-DD 포맷)"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # [추가] 현재 유저 가져오기
):
    # [수정] current_user.id 전달
    return StatisticsService.get_monthly_statistics(db, current_user.id, date)