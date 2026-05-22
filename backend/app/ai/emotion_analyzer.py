from transformers import pipeline

emotion_pipeline = pipeline(
    "text-classification",
    model="dlckdfuf141/korean-emotion-kluebert-v2",
    top_k=None
)

emotion_labels = {
    0: "공포",
    1: "놀람",
    2: "분노",
    3: "슬픔",
    4: "중립",
    5: "행복",
    6: "혐오"
}


def analyze_emotion(text: str):
    result = emotion_pipeline(text)[0]

    converted_result = []

    for emotion in result:
        converted_result.append({
            "label": emotion_labels[int(emotion["label"])],
            "score": emotion["score"]
        })

    return converted_result


def analyze_emotion_for_db(text: str):
    result = analyze_emotion(text)

    emotion_scores = {
        "fear": 0.0,
        "surprise": 0.0,
        "anger": 0.0,
        "sadness": 0.0,
        "neutral": 0.0,
        "happiness": 0.0,
        "disgust": 0.0,
    }

    label_to_field = {
        "공포": "fear",
        "놀람": "surprise",
        "분노": "anger",
        "슬픔": "sadness",
        "중립": "neutral",
        "행복": "happiness",
        "혐오": "disgust",
    }

    for emotion in result:
        field_name = label_to_field[emotion["label"]]
        emotion_scores[field_name] = emotion["score"]

    dominant_emotion = result[0]["label"]

    return {
        **emotion_scores,
        "dominant_emotion": dominant_emotion
    }


if __name__ == "__main__":
    test_text = "오늘은 정말 행복하고 기분이 좋았다."

    result = analyze_emotion(test_text)

    for emotion in result:
        print(emotion)