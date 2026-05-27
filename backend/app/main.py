from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.user import models as user_models
from app.diary import models as diary_models
from app.emotion import models as emotion_models
from app.survey import models as survey_models

from app.user.router import router as user_router
from app.diary.router import router as diary_router
from app.emotion.router import router as emotion_router
from app.survey.router import router as survey_router
# 새로 추가된 통계 라우터
from app.statistics.router import router as statistics_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="InnerNote API",
    description="InnerNote Backend API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(diary_router)
app.include_router(emotion_router)
app.include_router(survey_router)
# 메인 앱에 통계 라우터 등록
app.include_router(statistics_router)


@app.get("/")
def root():
    return {"message": "InnerNote API Server"}