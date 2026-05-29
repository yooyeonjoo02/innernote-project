from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import timedelta, datetime
from ytmusicapi import YTMusic
import requests
import random
import os                  # 👈 1. 이 한 줄 추가 (운영체제 시스템 기능 사용)
from dotenv import load_dotenv  # 👈 2. 이 한 줄 추가 (금고 여는 도구 가져오기)

from app.database import get_db
from app.diary.models import Diary
from app.survey.models import Survey

router = APIRouter(
    prefix="/api/v1/statistics",
    tags=["statistics"]
)

# 유튜브 뮤직 객체 초기화
ytmusic = YTMusic()

# 💡 3. .env 파일(비밀 금고) 열기 실행
load_dotenv()

# 💡 4. 금고 안에서 KAKAO_REST_API_KEY라는 이름으로 저장된 진짜 키 꺼내오기
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")


@router.get("/daily")
async def get_daily_statistics(
    date: str = Query(..., description="조회 대상 일자 (YYYY-MM-DD 포맷)"),
    db: Session = Depends(get_db)
):
    # 1. DB에서 해당 날짜의 최신 일기 조회 (한국 시간 9동기화)
    diary_record = db.query(Diary).filter(
        cast(Diary.created_at + timedelta(hours=9), Date) == date,
        Diary.is_deleted == False
    ).order_by(Diary.created_at.desc()).first()

    # 1-1. 일기가 없는 경우 처리
    if not diary_record:
        return {
            "status": "success",
            "data": {
                "diary_info": {
                    "diary_id": 0,
                    "diary_date": date,
                    "diary_content": "해당 날짜에 작성된 일기가 없습니다."
                },
                "emotion_analysis": [{"emotion_name": "대기", "ratio": 100}],
                "recommendations": {
                    "place": {"place_name": "-", "address": "-", "reason": "일기를 작성하시면 맞춤 장소를 추천해 드립니다.", "place_url": ""},
                    "playlist": [],
                    "mission": {"mission_type": "대기", "mission_content": "일기를 먼저 작성해 주세요."}
                }
            }
        }

    # 2. 일기 작성자의 설문조사(Survey) 데이터 연동 (완전 연동 시작)
    survey_record = db.query(Survey).filter(
        Survey.user_id == diary_record.user_id
    ).first()

    # 유저 개인 설정값 추출 (DB 데이터가 없으면 확실한 기본값 적용)
    favorite_artist = survey_record.favorite_singer if (survey_record and survey_record.favorite_singer) else "DAY6"
    residence_area = survey_record.residence_area if (survey_record and survey_record.residence_area) else "단국대"
    favorite_place = survey_record.favorite_place if (survey_record and survey_record.favorite_place) else "카페"
    want_to_go_place = survey_record.want_to_go_place if (survey_record and survey_record.want_to_go_place) else ""

    # 현재 일기의 주 감정 상태 추출
    primary_emotion = diary_record.emotion if diary_record.emotion else "평범"

    # ==========================================
    # [1] 장소 추천 연동 로직 (유저 지역 + 유저 성향 + 감정 키워드 조합)
    # ==========================================
    # 감정별 공간 무드 매핑
    emotion_place_mood = {
        "행복": "분위기 좋은 맛집", 
        "슬픔": "조용하고 아늑한 카페", 
        "분노": "산책하기 좋은 공원",
        "놀람": "편안한 서점", 
        "평범": "쉬기 좋은 수목원", 
        "혐오": "조용한 미술관"
    }
    mood_keyword = emotion_place_mood.get(primary_emotion, "편안한 장소")
    
    # 유저가 가고 싶어 했던 장소 유형이 있다면 우선 반영
    user_target_spot = want_to_go_place if want_to_go_place else favorite_place
    
    # 최종 카카오 검색 쿼리 빌드 (예: "용인시 죽전동 조용하고 아늑한 카페")
    kakao_search_query = f"{residence_area} {mood_keyword}"
    kakao_url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={kakao_search_query}&size=1"
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}

    try:
        response = requests.get(kakao_url, headers=headers)
        if response.status_code == 200 and response.json().get('documents'):
            place_data = response.json()['documents'][0]
            recommended_place_name = place_data['place_name']
            recommended_place_address = place_data.get('road_address_name') or place_data.get('address_name')
            place_url = place_data['place_url']
        else:
            # 검색 결과가 없을 경우 유저 성향을 조합한 동적 대체 텍스트 생성
            recommended_place_name = f"{residence_area} 주변 {user_target_spot}"
            recommended_place_address = f"{residence_area} 근처에서 편안한 시간을 보내보세요."
            place_url = f"https://map.kakao.com/link/search/{kakao_search_query}"
    except Exception:
        recommended_place_name = f"{residence_area} 주변 {user_target_spot}"
        recommended_place_address = "위치 서비스 통신 지연"
        place_url = "https://map.kakao.com"

    # ==========================================
    # [2] 음악 추천 연동 로직 (유저 선호 가수 + 감정 무드 실시간 검색)
    # ==========================================
    emotion_music_mood = {
        "행복": "신나는", "슬픔": "위로가 되는", "분노": "스트레스 풀리는",
        "놀람": "잔잔한", "평범": "편안한", "혐오": "기분 전환"
    }
    music_keyword = emotion_music_mood.get(primary_emotion, "편안한")
    
    # 유튜브 뮤직 최종 검색 쿼리 빌드 (예: "DAY6 위로가 되는 플레이리스트")
    youtube_search_query = f"{favorite_artist} {music_keyword} 플레이리스트"
    try:
        search_results = ytmusic.search(youtube_search_query, filter="playlists", limit=2)
        dynamic_playlist = []
        for idx, result in enumerate(search_results):
            dynamic_playlist.append({
                "music_id": idx + 1,
                "title": result.get('title', f'{favorite_artist} 추천 음악'),
                "artist": result.get('author', 'YouTube Music'),
                "youtube_url": f"https://music.youtube.com/playlist?list={result.get('browseId')}"
            })
    except Exception:
        dynamic_playlist = [{
            "music_id": 1, 
            "title": f"{favorite_artist}의 {music_keyword} 힐링 트랙", 
            "artist": "YouTube Music", 
            "youtube_url": "https://music.youtube.com"
        }]

    # ==========================================
    # [3] 미션 추천 연동 로직 (하드코딩 전면 제거, 데이터 융합형 미션 생성)
    # ==========================================
    # 유저의 거주 지역과 추천된 진짜 장소 이름을 문장 속에 동적으로 조립합니다.
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
        "평범": [
            f"무난한 하루도 소중합니다. 평소 가보고 싶었던 {recommended_place_name}에 들러 일상의 작은 변화를 만들어보세요.",
            f"선호하는 공간인 {user_target_spot} 테마에 맞춰 {residence_area} 근처에서 새로운 아지트를 발굴해 보세요."
            ],
        "혐오": [
            f"부정적인 잔상을 지워내기 위해 깔끔하게 정돈된 {recommended_place_name}에서 기분 전환을 시도해보세요.",
            f"내 취향의 음악과 장소에 집중할 시간입니다. {favorite_artist}의 노래를 들으며 감정 정화 스케줄을 소화해보세요."
        ]
    }
    
    # 일기 ID를 시드로 사용하여 매번 바뀌되 고정된 동적 미션 하나를 선택
    missions = emotion_mission_pool.get(primary_emotion, [f"{residence_area} 주변에서 휴식을 취해보세요."])
    selected_mission_content = missions[diary_record.id % len(missions)]

    # 4. 최종 데이터 팩킹 반환
    return {
        "status": "success",
        "data": {
            "diary_info": {
                "diary_id": diary_record.id,
                "diary_date": date,
                "diary_content": diary_record.content
            },
            "emotion_analysis": [
                {"emotion_name": primary_emotion, "ratio": 70},
                {"emotion_name": "기타", "ratio": 30}
            ],
            "recommendations": {
                "place": {
                    "place_name": recommended_place_name,
                    "address": recommended_place_address,
                    "reason": f"오늘 주한님의 {primary_emotion} 감정을 케어하기 위해 유저 설문 기반 무드로 엄선한 장소입니다.",
                    "place_url": place_url
                },
                "playlist": dynamic_playlist,
                "mission": {
                    "mission_type": "맞춤형 감정 액션",
                    "mission_content": selected_mission_content
                }
            }
        }
    }


@router.get("/period")
async def get_period_statistics(
    date: str = Query(..., description="조회 기준 마감 일자 (YYYY-MM-DD)"),
    period: int = Query(..., description="누적 통계 범위 설정 일수 (7 또는 30)"),
    db: Session = Depends(get_db)
):
    end_date = datetime.strptime(date, "%Y-%m-%d").date()
    start_date = end_date - timedelta(days=period - 1)

    diaries = db.query(Diary).filter(
        cast(Diary.created_at + timedelta(hours=9), Date) >= start_date,
        cast(Diary.created_at + timedelta(hours=9), Date) <= end_date,
        Diary.is_deleted == False
    ).all()

    emotion_count = {}
    total = 0
    for diary in diaries:
        if diary.emotion:
            emotion_count[diary.emotion] = emotion_count.get(diary.emotion, 0) + 1
            total += 1

    all_emotions = ["행복", "평범", "놀람", "슬픔", "분노", "혐오"]

    if total == 0:
        aggregated = [{"emotion_name": e, "ratio": 0} for e in all_emotions]
    else:
        aggregated = []
        assigned = 0
        for i, emotion in enumerate(all_emotions):
            count = emotion_count.get(emotion, 0)
            if i == len(all_emotions) - 1:
                ratio = 100 - assigned
            else:
                ratio = round(count / total * 100)
                assigned += ratio
            aggregated.append({"emotion_name": emotion, "ratio": ratio})

    return {
        "status": "success",
        "data": {
            "target_period": f"{period} days",
            "description": f"선택일 기준 최근 {period}일간의 누적 감정 통계 데이터입니다.",
            "aggregated_emotion_analysis": aggregated
        }
    }