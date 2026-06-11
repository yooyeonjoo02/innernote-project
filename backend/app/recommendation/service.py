import os
import random
import requests
from datetime import date, timezone, timedelta
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

        # 행복도 가져오기 (0.0 ~ 1.0 기준)
        happiness = emotion.happiness or 0.0

        # [수정 완료] 새로운 음악 키워드 생성 로직
        if happiness <= 0.5:
            recommendation_type = "comfort"
            comfort_keywords = []
            
            # 가수와 장르를 각각 독립적인 검색어로 추가하여 번갈아 나오도록 설정
            if survey.favorite_singer:
                comfort_keywords.append(f"{survey.favorite_singer} 힐링 노래")
                comfort_keywords.append(f"{survey.favorite_singer} 라이브 무대")
            if survey.favorite_genre:
                comfort_keywords.append(f"{survey.favorite_genre} 힐링 노래")
                comfort_keywords.append(f"{survey.favorite_genre} 명곡 추천")
            
            # 설문 정보가 비어있을 경우의 기본값
            if not comfort_keywords:
                comfort_keywords = ["잔잔한 힐링 노래", "마음이 편안해지는 음악"]
                
            music_keyword = random.choice(comfort_keywords)
        else:
            recommendation_type = "challenge"
            challenge_keywords = [
                "최신 신곡 추천", 
                "인기 급상승 음악", 
                "요즘 뜨는 트렌딩 노래", 
                "기분 좋아지는 신나는 노래"
            ]
            music_keyword = random.choice(challenge_keywords)

        # 💡 감정(일기 내용) 변경 및 설문 변경 감지 로직
        need_refresh = False
        
        survey_updated = getattr(survey, "updated_at", None)
        emotion_updated = getattr(emotion, "updated_at", None)
        diary_updated = getattr(diary, "updated_at", None)
        
        if diary_updated:
            diary_aware = diary_updated.replace(tzinfo=timezone.utc) if diary_updated.tzinfo is None else diary_updated
            
            if emotion_updated:
                emotion_aware = emotion_updated.replace(tzinfo=timezone.utc) if emotion_updated.tzinfo is None else emotion_updated
                if emotion_aware >= diary_aware:
                    need_refresh = True
            
            if target_date >= date.today() and survey_updated and not need_refresh:
                survey_aware = survey_updated.replace(tzinfo=timezone.utc) if survey_updated.tzinfo is None else survey_updated
                if survey_aware > diary_aware:
                    need_refresh = True

        db_needs_commit = False

        # --- 1. 음악 추천 ---
        if diary.recommended_music_title and diary.recommended_music_url and not need_refresh:
            music = MusicRecommendation(title=diary.recommended_music_title, url=diary.recommended_music_url)
        else:
            # 최근 14일(2주) 동안 추천된 음악 목록 가져오기
            recent_music = RecommendationRepository.find_recent_recommended_music(db, user_id, target_date, days=14)
            
            music = self._search_youtube_music(music_keyword, recent_titles=recent_music)
            diary.recommended_music_title = music.title
            diary.recommended_music_url = music.url
            db_needs_commit = True

        # --- 2. 장소 추천 ---
        if diary.recommended_place_name and not need_refresh:
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
            db_needs_commit = True

        # --- 3. 미션 추천 ---
        if diary.recommended_mission_title and not need_refresh:
            mission = MissionRecommendation(
                title=diary.recommended_mission_title,
                description=diary.recommended_mission_description
            )
        else:
            mission = self._build_mission(db=db, user_id=user_id, recommendation_type=recommendation_type, target_date=target_date)
            diary.recommended_mission_title = mission.title
            diary.recommended_mission_description = mission.description
            db_needs_commit = True

        # --- 4. 변경사항 커밋 ---
        if db_needs_commit:
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

    # 더 이상 필요 없는 로직이므로 삭제 무방하나, 구조 유지를 원하시면 놔두셔도 됩니다.
    def _pick_new_genre(self, favorite_genre: str):
        genres = ["발라드", "힙합", "재즈", "인디", "클래식", "알앤비", "락", "팝"]
        candidates = [g for g in genres if g != favorite_genre]
        return random.choice(candidates) if candidates else "어쿠스틱"

    def _search_youtube_music(self, keyword: str, recent_titles: list = None):
        if recent_titles is None:
            recent_titles = []
            
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
        # 넉넉하게 15개를 가져와서 필터링
        params = {"part": "snippet", "q": keyword, "type": "video", "maxResults": 15, "key": youtube_api_key}
        
        try:
            response = requests.get(url, params=params, timeout=5)
        except Exception:
            return MusicRecommendation(
                title=f"{keyword} 검색 결과",
                url=f"https://www.youtube.com/results?search_query={encoded_keyword}"
            )

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

        # 💡 [핵심] 최근 2주 동안 추천한 제목과 일치하는 영상 제거
        valid_items = [
            item for item in items 
            if item.get("snippet", {}).get("title") not in recent_titles
        ]
        
        # 만약 전부 겹쳐서 남은게 없다면 안전장치로 기존 items 그대로 사용
        if not valid_items:
            valid_items = items

        selected = random.choice(valid_items)
        title = selected.get("snippet", {}).get("title", f"{keyword} 추천 음악")
        video_id = selected.get("id", {}).get("videoId")
        
        return MusicRecommendation(title=title, url=f"https://www.youtube.com/watch?v={video_id}")

    def _search_kakao_place(self, db: Session, user_id: int, survey, happiness: float, target_date: date):
        # (기존 장소 추천 코드와 완전히 동일)
        kakao_api_key = settings.KAKAO_REST_API_KEY
        is_happy = happiness > 0.5
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
            return fallback

        url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
        params = {"query": query, "size": 15}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=5)
        except Exception:
            return fallback

        if response.status_code != 200:
            return fallback
            
        documents = response.json().get("documents", [])
        if not documents:
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

        return PlaceRecommendation(
            name=best_place.get("place_name"),
            address=best_place.get("road_address_name") or best_place.get("address_name"),
            url=best_place.get("place_url")
        )

    def _build_mission(self, db: Session, user_id: int, recommendation_type: str, target_date: date):
        # (기존 미션 추천 코드와 완전히 동일)
        recent_missions = RecommendationRepository.find_recent_recommended_missions(
            db, user_id, target_date, limit=10
        )
        mission_pool = COMFORT_MISSIONS if recommendation_type == "comfort" else CHALLENGE_MISSIONS
        valid_missions = [m for m in mission_pool if m["title"] not in recent_missions]
        if not valid_missions:
            valid_missions = mission_pool
        selected = random.choice(valid_missions)
        return MissionRecommendation(title=selected["title"], description=selected["description"])