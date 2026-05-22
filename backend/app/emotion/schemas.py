from pydantic import BaseModel


class EmotionCreateRequestDTO(BaseModel):
    diary_id: int

    fear: float
    surprise: float
    anger: float
    sadness: float
    neutral: float
    happiness: float
    disgust: float

    dominant_emotion: str


class EmotionResponseDTO(BaseModel):
    id: int

    diary_id: int

    fear: float
    surprise: float
    anger: float
    sadness: float
    neutral: float
    happiness: float
    disgust: float

    dominant_emotion: str

    class Config:
        from_attributes = True