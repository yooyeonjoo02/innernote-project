import os
import random
import requests
from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from urllib.parse import quote

from app.core.config import settings
from app.recommendation.repository import RecommendationRepository
from app.recommendation.mission_data import COMFORT_MISSIONS, CHALLENGE_MISSIONS
from app.recommendation.schemas import (
    DailyRecommendationResponse,
    MusicRecommendation,
    PlaceRecommendation,
    MissionRecommendation
)


class RecommendationService:

    def get_daily_recommendation(self, db: Session, user_id: int, target_date: date):
        diary = RecommendationRepository.find_diary_by_user_and_date(db=db, user_id=user_id, target_date=target_date)
        if diary is None:
            raise HTTPException(status_code=404, detail="해당 날짜의 일기가 없습니다.")

        emotion = RecommendationRepository.find_emotion_by_diary_id(db=db, diary_id=diary.id)
        if emotion is None:
            raise HTTPException(status_code=404, detail="해당 일기의 감정 분석 결과가 없습니다.")

        survey = RecommendationRepository.find_survey_by_user_id(db=db, user_id=user_id)
        if survey is None:
            raise HTTPException(status_code=404, detail="설문 정보가 없습니다.")

        happiness = emotion.happiness or 0.0

        if happiness <= 0.6:
            recommendation_type = "comfort"
            music_keyword = f"{survey.favorite_singer} {survey.favorite_genre} 힐링 노래"
        else:
            recommendation_type = "challenge"
            new_genre = self._pick_new_genre(survey.favorite_genre)
            music_keyword = f"기분 좋은 {new_genre} 노래 추천"

        if diary.recommended_music_title and diary.recommended_music_url:
            music = MusicRecommendation(title=diary.recommended_music_title, url=diary.recommended_music_url)
        else:
            music = self._search_youtube_music(music_keyword)
            diary.recommended_music_title = music.title
            diary.recommended_music_url = music.url
            db.commit()

        if diary.recommended_place_name:
            place = PlaceRecommendation(
                name=diary.recommended_place_name,
                address=diary.recommended_place_address,
                url=diary.recommended_place_url
            )
        else:
            place = self._search_kakao_place(db=db, user_id=user_id, survey=survey, happiness=happiness, target_date=target_date)
            diary.recommended_place_name = place.name
            diary.recommended_place_address = place.address
            diary.recommended_place_url = place.url
            db.commit()

        if diary.recommended_mission_title:
            mission = MissionRecommendation(
                title=diary.recommended_mission_title,
                description=diary.recommended_mission_description
            )
        else:
            mission = self._build_mission(db=db, user_id=user_id, recommendation_type=recommendation_type, target_date=target_date)
            diary.recommended_mission_title = mission.title
            diary.recommended_mission_description = mission.description
            db.commit()
            db.refresh(diary)

        return DailyRecommendationResponse(
            target_date=str(target_date),
            happiness=happiness,
            recommendation_type=recommendation_type,
            music=music,
            place=place,
            mission=mission
        )

    def _pick_new_genre(self, favorite_genre: str):
        genres = ["발라드", "힙합", "재즈", "인디", "클래식", "알앤비", "락", "팝"]
        candidates = [g for g in genres if g != favorite_genre]
        return random.choice(candidates) if candidates else "어쿠스틱"

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
        params = {"part": "snippet", "q": keyword, "type": "video", "maxResults": 10, "key": youtube_api_key}
        response = requests.get(url, params=params, timeout=5)

        if response.status_code != 200:
            return MusicRecommendation(
                title=f"{keyword} 검색 결과",
                url=f"https://www.youtube.com/results?search_query={encoded_keyword}"
            )

        items = response.json().get("items", [])
        if not items:
            return MusicRecommendation(
                title=f"{keyword} 검색 결과",
                url=f"https://www.youtube.com/results?search_query={encoded_keyword}"
            )

        selected = random.choice(items)
        title = selected.get("snippet", {}).get("title", f"{keyword} 추천 음악")
        video_id = selected.get("id", {}).get("videoId")
        return MusicRecommendation(title=title, url=f"https://www.youtube.com/watch?v={video_id}")

    def _search_kakao_place(self, db: Session, user_id: int, survey, happiness: float, target_date: date):
        kakao_api_key = settings.KAKAO_REST_API_KEY

        # ===== 디버그 로그 =====
        print(f"[DEBUG] kakao_api_key: {kakao_api_key[:10] if kakao_api_key else 'None'}")
        print(f"[DEBUG] residence: {survey.residence_area}")
        print(f"[DEBUG] fav_place: {survey.favorite_place}")
        print(f"[DEBUG] want_place: {survey.want_to_go_place}")
        # ======================

        is_happy = happiness >= 0.6
        residence = survey.residence_area or "용인시 수지구"
        fav_place = survey.favorite_place or "카페"
        want_place = survey.want_to_go_place or "명소"

        query = f"{residence} {want_place if is_happy else fav_place}".strip()
        encoded_query = quote(query)

        fallback = PlaceRecommendation(
            name=f"{residence} {want_place if is_happy else fav_place}",
            address=residence,
            url=f"https://map.kakao.com/?q={encoded_query}"
        )

        if not kakao_api_key:
            print("[DEBUG] API 키 없음 → fallback 반환")
            return fallback

        url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
        params = {"query": query, "size": 15}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=5)
        except Exception as e:
            print(f"[DEBUG] 요청 예외: {e}")
            return fallback

        # ===== 디버그 로그 =====
        print(f"[DEBUG] 카카오 응답코드: {response.status_code}")
        documents = response.json().get("documents", [])
        print(f"[DEBUG] 결과 수: {len(documents)}")
        if documents:
            print(f"[DEBUG] 첫번째 장소: {documents[0].get('place_name')}")
            print(f"[DEBUG] 두번째 장소: {documents[1].get('place_name') if len(documents) > 1 else 'N/A'}")
        # ======================

        if response.status_code != 200 or not documents:
            return fallback

        recent_places = RecommendationRepository.find_recent_recommended_places(
            db, user_id, target_date, days=21
        )

        valid_candidates = [
            doc for doc in documents
            if doc.get("place_name", "") not in recent_places
            and doc.get("place_name", "").replace(" ", "") != query.replace(" ", "")
        ]

        if not valid_candidates:
            valid_candidates = documents

        def score_place(index, place):
            score = 0
            review_count = int(place.get("review_count", 0) or 0)
            score += min(review_count, 500) * 0.1
            place_name = place.get("place_name", "")
            category = place.get("category_name", "")
            combined = place_name + " " + category
            if fav_place in combined:
                score += 20 if not is_happy else 10
            if want_place in combined:
                score += 20 if is_happy else 10
            score += max(0, 15 - index)
            return score

        scored = sorted(
            enumerate(valid_candidates),
            key=lambda x: score_place(x[0], x[1]),
            reverse=True
        )

        best_place = scored[0][1]
        print(f"[DEBUG] 최종 선택 장소: {best_place.get('place_name')}")

        return PlaceRecommendation(
            name=best_place.get("place_name"),
            address=best_place.get("road_address_name") or best_place.get("address_name"),
            url=best_place.get("place_url")
        )

    def _build_mission(self, db: Session, user_id: int, recommendation_type: str, target_date: date):
        recent_missions = RecommendationRepository.find_recent_recommended_missions(
            db, user_id, target_date, limit=10
        )
        mission_pool = COMFORT_MISSIONS if recommendation_type == "comfort" else CHALLENGE_MISSIONS
        valid_missions = [m for m in mission_pool if m["title"] not in recent_missions]
        if not valid_missions:
            valid_missions = mission_pool
        selected = random.choice(valid_missions)
        return MissionRecommendation(title=selected["title"], description=selected["description"])