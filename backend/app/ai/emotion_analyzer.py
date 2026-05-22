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


if __name__ == "__main__":

    test_text = "오늘은 정말 행복하고 기분이 좋았다."

    result = analyze_emotion(test_text)

    for emotion in result:
        print(emotion)