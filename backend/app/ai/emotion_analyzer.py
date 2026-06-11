from transformers import AutoTokenizer, AutoModelForSequenceClassification
from kiwipiepy import Kiwi
import torch
import torch.nn.functional as F
import re

MODEL_PATH = "kang192/innernote-emotion-kluebert"
# MODEL_PATH = "dlckdfuf141/korean-emotion-kluebert-v2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()
kiwi = Kiwi()

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

TEMPERATURE = 2.5
MAX_CHARS = 300
STRIDE = 200
MIN_KOREAN_CHARS = 2
MIN_TEXT_LEN = 3
CONFIDENCE_THRESHOLD = 0.25
# 조사/어미/용언이 하나도 없으면 명사 나열(가나다라마바사 등)로 판단
_FUNCTIONAL_TAGS = {
    'JKS','JKO','JKC','JKG','JKB','JX','JC',
    'EP','EF','EC','ETM','ETN',
    'XSV','XSA','VCP','VCN','VX','VA','VV',
}

_NEUTRAL_RESULT = {
    "fear": 0.0, "surprise": 0.0, "anger": 0.0,
    "sadness": 0.0, "neutral": 1.0,
    "happiness": 0.0, "disgust": 0.0,
    "dominant_emotion": "중립"
}


def _is_valid_input(text: str) -> bool:
    stripped = text.strip()

    if len(stripped) < MIN_TEXT_LEN:
        return False

    if len(re.findall(r'[가-힣]', stripped)) < MIN_KOREAN_CHARS:
        return False

    total = len(stripped.replace(' ', ''))
    korean = len(re.findall(r'[가-힣ㄱ-ㅎㅏ-ㅣ]', stripped))
    if total and (korean / total) < 0.2:
        return False

    # 조사/어미/용언 없이 명사만 나열된 입력 차단 (가나다라마바사 등)
    tokens = kiwi.analyze(stripped)[0][0]
    if not any(t.tag in _FUNCTIONAL_TAGS for t in tokens):
        return False

    return True


def analyze_emotion_for_db(text: str) -> dict:
    # ── 입력 검증 ──────────────────────────────────────────────────────
    if not _is_valid_input(text):
        return _NEUTRAL_RESULT

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

    # ── 신뢰도 낮은 OOD 입력 → 중립 처리 ────────────────────────────
    if float(avg_probs.max()) < CONFIDENCE_THRESHOLD:
        return _NEUTRAL_RESULT

    result = {label_map[i]: float(p) for i, p in enumerate(avg_probs)}
    dominant_idx = torch.argmax(avg_probs).item()
    result["dominant_emotion"] = korean_label_map[label_map[dominant_idx]]

    return result
