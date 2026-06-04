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
from app.statistics.router import router as statistics_router
from app.recommendation.router import router as recommendation_router

# 2. 현재 파일 구조에 맞춰 테이블을 완벽하게 새로 생성
Base.metadata.create_all(bind=engine)
# ==================================


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
app.include_router(statistics_router)
app.include_router(recommendation_router)


@app.get("/")
def root():
    return {"message": "InnerNote API Server"}