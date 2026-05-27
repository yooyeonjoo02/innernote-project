from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

MODEL_NAME = "dlckdfuf141/korean-emotion-kluebert-v2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

label_map = {
    0: "fear",
    1: "surprise",
    2: "anger",
    3: "sadness",
    4: "neutral",
    5: "happiness",
    6: "disgust"
}

korean_label_map = {
    "fear": "공포",
    "surprise": "놀람",
    "anger": "분노",
    "sadness": "슬픔",
    "neutral": "중립",
    "happiness": "행복",
    "disgust": "혐오"
}

TEMPERATURE = 5.0


def analyze_emotion_for_db(text: str):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits

    probabilities = F.softmax(
        logits / TEMPERATURE,
        dim=-1
    )[0]

    result = {}

    for idx, prob in enumerate(probabilities):
        result[label_map[idx]] = float(prob)

    dominant_idx = torch.argmax(probabilities).item()

    dominant_key = label_map[dominant_idx]

    result["dominant_emotion"] = korean_label_map[dominant_key]

    return result