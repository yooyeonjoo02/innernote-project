from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.statistics.service import StatisticsService


router = APIRouter(
    prefix="/api/v1/statistics",
    tags=["statistics"]
)


@router.get("/daily")
async def get_daily_statistics(
    date: str = Query(..., description="조회 대상 일자 (YYYY-MM-DD 포맷)"),
    db: Session = Depends(get_db)
):
    return StatisticsService.get_daily_statistics(db, date)


@router.get("/weekly")
async def get_weekly_statistics(
    date: str = Query(..., description="조회 기준 일자 (YYYY-MM-DD 포맷)"),
    db: Session = Depends(get_db)
):
    return StatisticsService.get_weekly_statistics(db, date)


@router.get("/monthly")
async def get_monthly_statistics(
    date: str = Query(..., description="조회 기준 일자 (YYYY-MM-DD 포맷)"),
    db: Session = Depends(get_db)
):
    return StatisticsService.get_monthly_statistics(db, date)