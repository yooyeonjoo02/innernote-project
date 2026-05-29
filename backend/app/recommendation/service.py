import os
import random
import requests
from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from urllib.parse import quote

from app.core.config import settings
from app.recommendation.repository import RecommendationRepository
from app.recommendation.schemas import (
    DailyRecommendationResponse,
    MusicRecommendation,
    PlaceRecommendation,
    MissionRecommendation
)


class RecommendationService:

    def get_daily_recommendation(
        self,
        db: Session,
        user_id: int,
        target_date: date
    ):
        diary = RecommendationRepository.find_diary_by_user_and_date(
            db=db,
            user_id=user_id,
            target_date=target_date
        )

        if diary is None:
            raise HTTPException(
                status_code=404,
                detail="해당 날짜의 일기가 없습니다."
            )

        emotion = RecommendationRepository.find_emotion_by_diary_id(
            db=db,
            diary_id=diary.id
        )

        if emotion is None:
            raise HTTPException(
                status_code=404,
                detail="해당 일기의 감정 분석 결과가 없습니다."
            )

        survey = RecommendationRepository.find_survey_by_user_id(
            db=db,
            user_id=user_id
        )

        if survey is None:
            raise HTTPException(
                status_code=404,
                detail="설문 정보가 없습니다."
            )

        happiness = emotion.happiness or 0.0

        if happiness <= 0.6:
            recommendation_type = "comfort"

            music_keyword = f"{survey.favorite_singer} 노래"
            place_keyword = survey.favorite_place
        else:
            recommendation_type = "challenge"

            new_genre = self._pick_new_genre(survey.favorite_genre)
            music_keyword = f"{new_genre} 노래 추천"
            place_keyword = survey.want_to_go_place

        music = self._search_youtube_music(music_keyword)

        place = self._search_kakao_place(
            keyword=place_keyword,
            address=survey.residence_area
        )

        mission = self._build_mission(
            recommendation_type=recommendation_type,
            favorite_singer=survey.favorite_singer,
            favorite_place=survey.favorite_place,
            residence_area=survey.residence_area,
            place_name=place.name,
            diary_id=diary.id
        )

        return DailyRecommendationResponse(
            target_date=str(target_date),
            happiness=happiness,
            recommendation_type=recommendation_type,
            music=music,
            place=place,
            mission=mission
        )

    def _pick_new_genre(self, favorite_genre: str):
        genres = [
            "발라드",
            "힙합",
            "재즈",
            "인디",
            "클래식",
            "알앤비",
            "락",
            "팝"
        ]

        candidates = [
            genre for genre in genres
            if genre != favorite_genre
        ]

        return random.choice(candidates)

    def _search_youtube_music(self, keyword: str):
        youtube_api_key = settings.YOUTUBE_API_KEY

        if not keyword:
            keyword = "오늘의 음악"

        encoded_keyword = quote(keyword)

        if not youtube_api_key:
            return MusicRecommendation(
                title=f"{keyword} 검색 결과",
                url=f"https://www.youtube.com/results?search_query={encoded_keyword}"
            )

        url = "https://www.googleapis.com/youtube/v3/search"

        params = {
            "part": "snippet",
            "q": keyword,
            "type": "video",
            "maxResults": 10,
            "key": youtube_api_key
        }

        response = requests.get(
            url,
            params=params,
            timeout=5
        )

        if response.status_code != 200:
            return MusicRecommendation(
                title=f"{keyword} 검색 결과",
                url=f"https://www.youtube.com/results?search_query={encoded_keyword}"
            )

        data = response.json()
        items = data.get("items", [])

        if not items:
            return MusicRecommendation(
                title=f"{keyword} 검색 결과",
                url=f"https://www.youtube.com/results?search_query={encoded_keyword}"
            )

        selected = random.choice(items)

        title = selected.get("snippet", {}).get("title", f"{keyword} 추천 음악")
        video_id = selected.get("id", {}).get("videoId")

        if not video_id:
            return MusicRecommendation(
                title=f"{keyword} 검색 결과",
                url=f"https://www.youtube.com/results?search_query={encoded_keyword}"
            )

        return MusicRecommendation(
            title=title,
            url=f"https://www.youtube.com/watch?v={video_id}"
        )

    def _search_kakao_place(self, keyword: str, address: str):
        kakao_api_key = os.getenv("KAKAO_REST_API_KEY")

        if not keyword:
            keyword = "카페"

        if not address:
            address = ""

        query = f"{address} {keyword}".strip()
        encoded_query = quote(query)

        if not kakao_api_key:
            return PlaceRecommendation(
                name=query,
                address=address,
                url=f"https://map.kakao.com/?q={encoded_query}"
            )

        url = "https://dapi.kakao.com/v2/local/search/keyword.json"

        headers = {
            "Authorization": f"KakaoAK {kakao_api_key}"
        }

        params = {
            "query": query,
            "size": 10
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=5
        )

        if response.status_code != 200:
            return PlaceRecommendation(
                name=query,
                address=address,
                url=f"https://map.kakao.com/?q={encoded_query}"
            )

        data = response.json()
        documents = data.get("documents", [])

        if not documents:
            return PlaceRecommendation(
                name=query,
                address=address,
                url=f"https://map.kakao.com/?q={encoded_query}"
            )

        place = random.choice(documents)

        return PlaceRecommendation(
            name=place.get("place_name"),
            address=place.get("road_address_name") or place.get("address_name"),
            url=place.get("place_url")
        )

    def _build_mission(
        self,
        recommendation_type: str,
        favorite_singer: str,
        favorite_place: str,
        residence_area: str,
        place_name: str,
        diary_id: int
    ):
        if recommendation_type == "comfort":
            missions = [
                {
                    "title": "좋아하는 음악 들으며 쉬기",
                    "description": f"{favorite_singer}의 노래를 들으며 오늘의 감정을 천천히 정리해보세요."
                },
                {
                    "title": "익숙한 공간에서 마음 쉬기",
                    "description": f"{place_name}에서 부담 없이 시간을 보내며 마음을 가라앉혀보세요."
                },
                {
                    "title": "짧은 감정 기록하기",
                    "description": "오늘 가장 크게 느낀 감정을 한 문장으로 적어보세요."
                }
            ]
        else:
            missions = [
                {
                    "title": "새로운 장소 방문하기",
                    "description": f"{residence_area} 근처에서 평소와 다른 공간을 경험해보세요."
                },
                {
                    "title": "새로운 음악 들어보기",
                    "description": "평소 자주 듣지 않던 장르의 노래를 한 곡 들어보세요."
                },
                {
                    "title": "작은 도전 하나 해보기",
                    "description": f"오늘은 {favorite_place}와는 다른 분위기의 장소를 찾아보세요."
                }
            ]

        selected = missions[diary_id % len(missions)]

        return MissionRecommendation(
            title=selected["title"],
            description=selected["description"]
        )