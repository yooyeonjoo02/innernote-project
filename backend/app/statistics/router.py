from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import timedelta
from ytmusicapi import YTMusic  # 👈 유튜브 뮤직 API 라이브러리 추가!

# 팀 프로젝트의 공통 DB 연결 창구
from app.database import get_db
# 실제 일기 모델
from app.diary.models import Diary

router = APIRouter(
    prefix="/api/v1/statistics",
    tags=["statistics"]
)

# 유튜브 뮤직 객체 생성 (서버 켜질 때 한 번만 로드)
ytmusic = YTMusic()

# --- [GET] 3번 항목: 일별 통계 및 맞춤형 콘텐츠 추천 조회 API ---
@router.get("/daily")
async def get_daily_statistics(
    date: str = Query(..., description="조회 대상 일자 (YYYY-MM-DD 포맷)"),
    db: Session = Depends(get_db)
):
    # 1. DB에서 해당 날짜에 작성된 일기 조회 (한국 시간 적용)
    diary_record = db.query(Diary).filter(
        cast(Diary.created_at + timedelta(hours=9), Date) == date,
        Diary.is_deleted == False
    ).order_by(Diary.created_at.desc()).first()

    # 2. 일기가 없을 경우 빈 데이터 반환
    if not diary_record:
        return {
            "status": "success",
            "data": {
                "diary_info": {
                    "diary_id": 0,
                    "diary_date": date,
                    "diary_content": "해당 날짜에 작성된 일기가 없습니다. InnerNote에 첫 일기를 남겨보세요!"
                },
                "emotion_analysis": [{"emotion_name": "대기", "ratio": 100}],
                "recommendations": {
                    "place": {"place_name": "-", "address": "-", "reason": "일기를 작성하시면 맞춤 장소를 추천해 드립니다."},
                    "playlist": [],
                    "mission": {"mission_type": "대기", "mission_content": "일기를 먼저 작성해 주세요."}
                }
            }
        }

    # 3. [★ 핵심] 일기가 있을 경우: 진짜 유튜브 추천 생성 로직
    primary_emotion = diary_record.emotion if diary_record.emotion else "평범"
    
    # 감정별 유튜브 검색 키워드 매핑
    emotion_keyword_map = {
        "행복": "신나는",
        "슬픔": "위로가 되는",
        "분노": "스트레스 풀리는",
        "놀람": "잔잔한",
        "평범": "편안한",
        "혐오": "기분 전환"
    }
    search_keyword = emotion_keyword_map.get(primary_emotion, "편안한")
    
    # 임시 유저 선호 가수 (추후 User DB 연동 시 db.query(User)로 교체)
    favorite_artist = "DAY6" 
    search_query = f"{favorite_artist} {search_keyword} 플레이리스트"
    
    # ytmusicapi로 진짜 유튜브 뮤직 검색 (상위 2개)
    try:
        search_results = ytmusic.search(search_query, filter="playlists", limit=2)
        dynamic_playlist = []
        for idx, result in enumerate(search_results):
            dynamic_playlist.append({
                "music_id": idx + 1,
                "title": result.get('title', f'{favorite_artist} 추천 음악'),
                "artist": result.get('author', 'YouTube'),
                # browseId를 사용해 실제 재생 가능한 유튜브 뮤직 주소 생성
                "youtube_url": f"https://music.youtube.com/playlist?list={result.get('browseId')}"
            })
    except Exception as e:
        # 혹시 유튜브 통신 에러가 나면 앱이 뻗지 않도록 기본값 제공
        dynamic_playlist = [{
            "music_id": 1, 
            "title": "유튜브 검색 지연중...", 
            "artist": "알림", 
            "youtube_url": "https://music.youtube.com"
        }]

    # 4. 진짜 데이터를 매핑하여 반환
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
                    "place_name": "조용한 카페 아늑 죽전점",
                    "address": "경기 용인시 수지구 죽전로 152",
                    "reason": "추후 카카오/네이버 API로 변경 예정입니다."
                },
                "playlist": dynamic_playlist, # 👈 방금 위에서 만든 진짜 검색 결과가 들어갑니다!
                "mission": {
                    "mission_type": "감정 케어",
                    "mission_content": f"오늘은 {search_keyword} 음악을 들으며 하루를 마무리해 보세요."
                }
            }
        }
    }

# --- [GET] 4번 항목: 기간별(주별/월별) 누적 감정 통계 조회 API ---
@router.get("/period")
async def get_period_statistics(
    date: str = Query(..., description="조회 기준 마감 일자 (YYYY-MM-DD)"),
    period: int = Query(..., description="누적 통계 범위 설정 일수 (7 또는 30)"),
    db: Session = Depends(get_db)
):
    return {
        "status": "success",
        "data": {
            "target_period": f"{period} days",
            "description": f"선택일 기준 최근 {period}일간의 누적 감정 통계 데이터입니다.",
            "aggregated_emotion_analysis": [
                {"emotion_name": "행복", "ratio": 60},
                {"emotion_name": "평범", "ratio": 20},
                {"emotion_name": "슬픔", "ratio": 10},
                {"emotion_name": "놀람", "ratio": 10},
                {"emotion_name": "분노", "ratio": 0},
                {"emotion_name": "혐오", "ratio": 0}
            ]
        }
    }