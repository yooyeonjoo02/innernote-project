# config file

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    
    SECRET_KEY: str = "innernote-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    KAKAO_REST_API_KEY: str = ""
    YOUTUBE_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()