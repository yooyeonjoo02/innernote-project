from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import calendar
import os
import requests

from dotenv import load_dotenv
from ytmusicapi import YTMusic

from app.statistics.repository import StatisticsRepository
from app.statistics.schemas import EMOTION_FIELDS, EMOTION_KOREAN_NAMES


load_dotenv()
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")

ytmusic = YTMusic()


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
            return [
                {
                    "emotion_key": field,
                    "emotion_name": EMOTION_KOREAN_NAMES[field],
                    "ratio": 0
                }
                for field in EMOTION_FIELDS
            ]

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
    def get_daily_statistics(db: Session, date: str):
        target_date = StatisticsService.parse_date(date)

        diary_record = StatisticsRepository.find_diary_by_date(
            db,
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
                    "dominant_emotion": None,
                    "recommendations": {
                        "place": {
                            "place_name": "-",
                            "address": "-",
                            "reason": "일기를 작성하시면 맞춤 장소를 추천해 드립니다.",
                            "place_url": ""
                        },
                        "playlist": [],
                        "mission": {
                            "mission_type": "대기",
                            "mission_content": "일기를 먼저 작성해 주세요."
                        }
                    }
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
                    "dominant_emotion": None,
                    "recommendations": {
                        "place": {
                            "place_name": "-",
                            "address": "-",
                            "reason": "감정 분석 결과가 아직 없습니다.",
                            "place_url": ""
                        },
                        "playlist": [],
                        "mission": {
                            "mission_type": "대기",
                            "mission_content": "감정 분석 후 추천을 확인할 수 있습니다."
                        }
                    }
                }
            }

        survey_record = StatisticsRepository.find_survey_by_user_id(
            db,
            diary_record.user_id
        )

        recommendation = StatisticsService.build_recommendation(
            diary_record,
            emotion_analysis,
            survey_record
        )

        return {
            "status": "success",
            "data": {
                "diary_info": {
                    "diary_id": diary_record.id,
                    "diary_date": date,
                    "diary_content": diary_record.content
                },
                "emotion_analysis": StatisticsService.emotion_to_list(emotion_analysis),
                "dominant_emotion": StatisticsService.get_dominant_emotion(emotion_analysis),
                "recommendations": recommendation
            }
        }

    @staticmethod
    def get_weekly_statistics(db: Session, date: str):
        end_date = StatisticsService.parse_date(date)
        start_date = end_date - timedelta(days=6)

        return StatisticsService.get_period_statistics(
            db,
            "weekly",
            start_date,
            end_date
        )

    @staticmethod
    def get_monthly_statistics(db: Session, date: str):
        target_date = StatisticsService.parse_date(date)
        start_date = target_date.replace(day=1)

        last_day = calendar.monthrange(
            target_date.year,
            target_date.month
        )[1]

        end_date = target_date.replace(day=last_day)

        return StatisticsService.get_period_statistics(
            db,
            "monthly",
            start_date,
            end_date
        )

    @staticmethod
    def get_period_statistics(
        db: Session,
        period: str,
        start_date,
        end_date
    ):
        diaries = StatisticsRepository.find_diaries_with_emotion_analysis(
            db,
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

    @staticmethod
    def build_recommendation(
        diary_record,
        emotion_analysis,
        survey_record
    ):
        favorite_artist = survey_record.favorite_singer if (survey_record and survey_record.favorite_singer) else "DAY6"
        residence_area = survey_record.residence_area if (survey_record and survey_record.residence_area) else "단국대"
        favorite_place = survey_record.favorite_place if (survey_record and survey_record.favorite_place) else "카페"
        want_to_go_place = survey_record.want_to_go_place if (survey_record and survey_record.want_to_go_place) else ""

        primary_emotion = StatisticsService.get_dominant_emotion(emotion_analysis)

        emotion_place_mood = {
            "행복": "분위기 좋은 맛집",
            "슬픔": "조용하고 아늑한 카페",
            "분노": "산책하기 좋은 공원",
            "놀람": "편안한 서점",
            "중립": "쉬기 좋은 수목원",
            "공포": "안정감을 주는 조용한 카페",
            "혐오": "조용한 미술관"
        }

        mood_keyword = emotion_place_mood.get(primary_emotion, "편안한 장소")
        user_target_spot = want_to_go_place if want_to_go_place else favorite_place

        kakao_search_query = f"{residence_area} {mood_keyword}"
        kakao_url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={kakao_search_query}&size=1"
        headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}

        try:
            response = requests.get(kakao_url, headers=headers)

            if response.status_code == 200 and response.json().get("documents"):
                place_data = response.json()["documents"][0]
                recommended_place_name = place_data["place_name"]
                recommended_place_address = place_data.get("road_address_name") or place_data.get("address_name")
                place_url = place_data["place_url"]
            else:
                recommended_place_name = f"{residence_area} 주변 {user_target_spot}"
                recommended_place_address = f"{residence_area} 근처에서 편안한 시간을 보내보세요."
                place_url = f"https://map.kakao.com/link/search/{kakao_search_query}"

        except Exception:
            recommended_place_name = f"{residence_area} 주변 {user_target_spot}"
            recommended_place_address = "위치 서비스 통신 지연"
            place_url = "https://map.kakao.com"

        emotion_music_mood = {
            "행복": "신나는",
            "슬픔": "위로가 되는",
            "분노": "스트레스 풀리는",
            "놀람": "잔잔한",
            "중립": "편안한",
            "공포": "안정되는",
            "혐오": "기분 전환"
        }

        music_keyword = emotion_music_mood.get(primary_emotion, "편안한")
        youtube_search_query = f"{favorite_artist} {music_keyword} 플레이리스트"

        try:
            search_results = ytmusic.search(
                youtube_search_query,
                filter="playlists",
                limit=2
            )

            dynamic_playlist = []

            for idx, result in enumerate(search_results):
                dynamic_playlist.append({
                    "music_id": idx + 1,
                    "title": result.get("title", f"{favorite_artist} 추천 음악"),
                    "artist": result.get("author", "YouTube Music"),
                    "youtube_url": f"https://music.youtube.com/playlist?list={result.get('browseId')}"
                })

        except Exception:
            dynamic_playlist = [{
                "music_id": 1,
                "title": f"{favorite_artist}의 {music_keyword} 힐링 트랙",
                "artist": "YouTube Music",
                "youtube_url": "https://music.youtube.com"
            }]

        emotion_mission_pool = {
            "행복": [
                f"오늘의 긍정적인 에너지를 이어가기 위해 {recommended_place_name}에 방문하여 나에게 작은 선물을 해보세요.",
                f"좋은 기분을 동력 삼아 {residence_area} 주변을 가볍게 산책하며 하늘 사진을 한 장 찍어보세요."
            ],
            "슬픔": [
                f"마음이 가라앉을 때는 따뜻한 음료가 도움이 됩니다. {recommended_place_name}에서 온전히 나만의 시간을 가져보세요.",
                f"좋아하는 가수 {favorite_artist}의 음악을 깊게 음미하며, 일기장에 슬픈 감정을 모두 털어내 보세요."
            ],
            "분노": [
                f"답답한 감정을 환기할 수 있도록 {recommended_place_name} 근처를 빠른 걸음으로 걸으며 스트레스를 날려보세요.",
                f"심호흡을 3번 크게 하고, 차분한 마음으로 {residence_area} 주변의 조용한 공간을 찾아 잠시 명상해보세요."
            ],
            "놀람": [
                f"감정의 진정을 위해 {recommended_place_name} 같은 차분한 공간에서 따뜻한 차 한 잔을 마셔보세요.",
                f"놀란 마음을 가라앉히고 편안한 일상으로 복귀하기 위해 익숙한 {residence_area} 거리를 걸어보세요."
            ],
            "중립": [
                f"무난한 하루도 소중합니다. 평소 가보고 싶었던 {recommended_place_name}에 들러 일상의 작은 변화를 만들어보세요.",
                f"선호하는 공간인 {user_target_spot} 테마에 맞춰 {residence_area} 근처에서 새로운 아지트를 발굴해 보세요."
            ],
            "공포": [
                f"불안한 마음을 진정시키기 위해 {recommended_place_name}에서 천천히 호흡하며 쉬어보세요.",
                f"{favorite_artist}의 차분한 음악을 들으며 오늘 느낀 감정을 짧게 정리해보세요."
            ],
            "혐오": [
                f"부정적인 잔상을 지워내기 위해 깔끔하게 정돈된 {recommended_place_name}에서 기분 전환을 시도해보세요.",
                f"내 취향의 음악과 장소에 집중할 시간입니다. {favorite_artist}의 노래를 들으며 감정 정화 스케줄을 소화해보세요."
            ]
        }

        missions = emotion_mission_pool.get(
            primary_emotion,
            [f"{residence_area} 주변에서 휴식을 취해보세요."]
        )

        selected_mission_content = missions[diary_record.id % len(missions)]

        return {
            "place": {
                "place_name": recommended_place_name,
                "address": recommended_place_address,
                "reason": f"오늘 사용자의 {primary_emotion} 감정을 케어하기 위해 유저 설문 기반 무드로 엄선한 장소입니다.",
                "place_url": place_url
            },
            "playlist": dynamic_playlist,
            "mission": {
                "mission_type": "맞춤형 감정 액션",
                "mission_content": selected_mission_content
            }
        }