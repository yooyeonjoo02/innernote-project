from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import calendar

from app.statistics.repository import StatisticsRepository
from app.statistics.schemas import EMOTION_FIELDS, EMOTION_KOREAN_NAMES


class StatisticsService:

    @staticmethod
    def parse_date(date_str: str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="날짜 형식은 YYYY-MM-DD 이어야 합니다."
            )

    @staticmethod
    def emotion_to_list(emotion_analysis):
        return [
            {
                "emotion_key": field,
                "emotion_name": EMOTION_KOREAN_NAMES[field],
                "ratio": round((getattr(emotion_analysis, field, 0.0) or 0.0) * 100, 2)
            }
            for field in EMOTION_FIELDS
        ]

    @staticmethod
    def empty_emotion_analysis():
        return [
            {
                "emotion_key": field,
                "emotion_name": EMOTION_KOREAN_NAMES[field],
                "ratio": 0
            }
            for field in EMOTION_FIELDS
        ]

    @staticmethod
    def get_dominant_emotion(emotion_analysis):
        if emotion_analysis.dominant_emotion:
            dominant = emotion_analysis.dominant_emotion

            if dominant in EMOTION_KOREAN_NAMES:
                return EMOTION_KOREAN_NAMES[dominant]

            return dominant

        max_field = max(
            EMOTION_FIELDS,
            key=lambda field: getattr(emotion_analysis, field, 0.0) or 0.0
        )

        return EMOTION_KOREAN_NAMES[max_field]

    @staticmethod
    def calculate_average_emotions(emotion_analyses):
        if not emotion_analyses:
            return StatisticsService.empty_emotion_analysis()

        result = []

        for field in EMOTION_FIELDS:
            total = sum(
                getattr(emotion_analysis, field, 0.0) or 0.0
                for emotion_analysis in emotion_analyses
            )

            average = total / len(emotion_analyses)

            result.append({
                "emotion_key": field,
                "emotion_name": EMOTION_KOREAN_NAMES[field],
                "ratio": round(average * 100, 2)
            })

        return result

    @staticmethod
    def get_dominant_emotion_from_average(average_emotions):
        if not average_emotions:
            return None

        max_emotion = max(
            average_emotions,
            key=lambda emotion: emotion["ratio"]
        )

        if max_emotion["ratio"] == 0:
            return None

        return max_emotion["emotion_name"]

    @staticmethod
    def build_daily_trend(diaries):
        trend = []

        for diary in diaries:
            emotion_analysis = diary.emotion_analysis

            if not emotion_analysis:
                continue

            trend.append({
                "date": diary.diary_date.isoformat(),
                "diary_id": diary.id,
                "dominant_emotion": StatisticsService.get_dominant_emotion(emotion_analysis),
                "emotions": StatisticsService.emotion_to_list(emotion_analysis)
            })

        return trend

    # [수정] user_id 파라미터 추가
    @staticmethod
    def get_daily_statistics(db: Session, user_id: int, date: str):
        target_date = StatisticsService.parse_date(date)

        # [수정] 레포지토리 호출 시 user_id 전달
        diary_record = StatisticsRepository.find_diary_by_date(
            db,
            user_id,
            target_date
        )

        if not diary_record:
            return {
                "status": "success",
                "data": {
                    "diary_info": {
                        "diary_id": 0,
                        "diary_date": date,
                        "diary_content": "해당 날짜에 작성된 일기가 없습니다."
                    },
                    "emotion_analysis": StatisticsService.empty_emotion_analysis(),
                    "dominant_emotion": None
                }
            }

        emotion_analysis = StatisticsRepository.find_emotion_analysis_by_diary_id(
            db,
            diary_record.id
        )

        if not emotion_analysis:
            return {
                "status": "success",
                "data": {
                    "diary_info": {
                        "diary_id": diary_record.id,
                        "diary_date": date,
                        "diary_content": diary_record.content
                    },
                    "emotion_analysis": StatisticsService.empty_emotion_analysis(),
                    "dominant_emotion": None
                }
            }

        return {
            "status": "success",
            "data": {
                "diary_info": {
                    "diary_id": diary_record.id,
                    "diary_date": date,
                    "diary_content": diary_record.content
                },
                "emotion_analysis": StatisticsService.emotion_to_list(emotion_analysis),
                "dominant_emotion": StatisticsService.get_dominant_emotion(emotion_analysis)
            }
        }

    # [수정] user_id 파라미터 추가 및 내부 함수에 전달
    @staticmethod
    def get_weekly_statistics(db: Session, user_id: int, date: str):
        end_date = StatisticsService.parse_date(date)
        start_date = end_date - timedelta(days=6)

        return StatisticsService.get_period_statistics(
            db,
            user_id,
            "weekly",
            start_date,
            end_date
        )

    # [수정] user_id 파라미터 추가 및 내부 함수에 전달
    @staticmethod
    def get_monthly_statistics(db: Session, user_id: int, date: str):
        target_date = StatisticsService.parse_date(date)
        start_date = target_date.replace(day=1)

        last_day = calendar.monthrange(
            target_date.year,
            target_date.month
        )[1]

        end_date = target_date.replace(day=last_day)

        return StatisticsService.get_period_statistics(
            db,
            user_id,
            "monthly",
            start_date,
            end_date
        )

    # [수정] user_id 파라미터 추가 및 레포지토리에 전달
    @staticmethod
    def get_period_statistics(
        db: Session,
        user_id: int,
        period: str,
        start_date,
        end_date
    ):
        diaries = StatisticsRepository.find_diaries_with_emotion_analysis(
            db,
            user_id,
            start_date,
            end_date
        )

        emotion_analyses = [
            diary.emotion_analysis
            for diary in diaries
            if diary.emotion_analysis
        ]

        average_emotions = StatisticsService.calculate_average_emotions(
            emotion_analyses
        )

        return {
            "status": "success",
            "data": {
                "period": period,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_diary_count": len(emotion_analyses),
                "dominant_emotion": StatisticsService.get_dominant_emotion_from_average(
                    average_emotions
                ),
                "average_emotions": average_emotions,
                "daily_trend": StatisticsService.build_daily_trend(diaries)
            }
        }