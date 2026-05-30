from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

MODEL_PATH = "kang192/innernote-emotion-kluebert"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

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
MAX_CHARS = 300
STRIDE = 200


def analyze_emotion_for_db(text: str) -> dict:
    chunks = [text] if len(text) <= MAX_CHARS else [
        text[i:i + MAX_CHARS]
        for i in range(0, len(text), STRIDE)
        if len(text[i:i + MAX_CHARS]) >= 30
    ]

    all_probs = []
    for chunk in chunks:
        inputs = tokenizer(
            chunk,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )
        with torch.no_grad():
            logits = model(**inputs).logits
        probs = F.softmax(logits / TEMPERATURE, dim=-1)[0]
        all_probs.append(probs)

    avg_probs = torch.stack(all_probs).mean(dim=0)

    result = {label_map[i]: float(p) for i, p in enumerate(avg_probs)}
    dominant_idx = torch.argmax(avg_probs).item()
    result["dominant_emotion"] = korean_label_map[label_map[dominant_idx]]

    return result
