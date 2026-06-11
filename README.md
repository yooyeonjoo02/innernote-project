# 📔 InnerNote (이너노트)

> **"바쁜 일상 속, 나의 감정을 기록하고 이해하는 맞춤형 감정 관리 서비스"**

InnerNote는 바쁜 현대인들이 자신의 감정을 기록하고, 장기적인 감정 흐름을 분석하며, 목표를 설정할 수 있도록 돕는 AI 기반 감정 관리 서비스입니다. 사용자의 감정 상태와 개인 취향을 종합적으로 분석하여 맞춤형 음악과 장소를 추천합니다.

---

# 📌 프로젝트 소개

현대인들은 바쁜 일상에 치여 정작 자신의 감정을 돌보지 못하는 경우가 많습니다.

InnerNote는 단순히 일상을 기록하는 다이어리를 넘어 사용자가 자신의 감정을 객관적으로 마주하고 관리할 수 있도록 돕기 위해 기획되었습니다.

작성된 일기를 AI가 분석하여 감정 상태를 파악하고, 사용자의 취향 데이터를 함께 활용하여 그날의 감정에 적합한 콘텐츠를 추천합니다.

이를 통해 사용자는 감정 변화를 지속적으로 기록하고, 스스로를 돌아보며 더 건강한 일상을 만들어갈 수 있습니다.

---

# ✨ 주요 기능

## 🔐 사용자 인증 및 보안

* 회원가입
* 로그인
* JWT 기반 사용자 인증
* 사용자 정보 조회 및 수정
* 회원 탈퇴 기능

---

## 📝 감정 일기 작성

* 달력 기반 일기 작성
* 날짜별 일기 조회
* 일기 수정 및 삭제
* AI 감정 분석 자동 수행
* 감정 비율 저장

---

## 📋 사용자 취향 설문

사용자의 취향 정보를 수집하여 추천 시스템에 활용합니다.

설문 항목

* 좋아하는 가수
* 좋아하는 음악 장르
* 거주 지역
* 자주 가는 장소
* 가보고 싶은 장소

---

## 🎵 AI 기반 콘텐츠 추천

### 음악 추천

* 사용자의 감정 상태 분석
* 선호 가수 및 음악 장르 반영
* YouTube Data API 기반 추천

### 장소 추천

* 사용자 거주 지역 기반 추천
* Kakao Local API 활용
* 감정 상태에 따른 맞춤 장소 추천

### 데일리 추천

* 긍정적인 하루를 위한 추천 콘텐츠 제공
* 사용자 감정에 따른 맞춤형 경험 제공

---

## 📊 감정 통계

* 일별 감정 통계
* 주별 감정 통계
* 월별 감정 통계
* 감정 비율 시각화
* 감정 변화 추이 확인

---

# 🏗️ 시스템 아키텍처

```text
Frontend (React + Vite)
        │
        ▼
Backend (FastAPI)
        │
 ┌──────┼──────┐
 ▼      ▼      ▼
Emotion Survey Recommendation
Analysis Data    System
        │
        ▼
PostgreSQL Database
```

---

# 🛠️ 기술 스택

| 분야            | 기술                                   |
| ------------- | ------------------------------------ |
| Frontend      | React, Vite                          |
| Backend       | Python, FastAPI                      |
| Database      | PostgreSQL, SQLAlchemy               |
| AI Model      | Hugging Face Transformers, KLUE-BERT |
| External API  | YouTube Data API v3, Kakao Local API |
| Collaboration | Git, GitHub, Jira, Confluence, Figma |

---

# 🤖 AI 감정 분석

사용자가 작성한 일기를 AI 모델이 분석하여 다음 7가지 감정에 대한 확률을 제공합니다.

* 😊 행복 (Happiness)
* 😐 중립 (Neutral)
* 😢 슬픔 (Sadness)
* 😠 분노 (Anger)
* 😨 공포 (Fear)
* 😲 놀람 (Surprise)
* 🤢 혐오 (Disgust)

KLUE-BERT 기반 감정 분석 모델을 활용하며, 추가 데이터셋을 통해 파인튜닝하여 성능을 향상시켰습니다.

---

# 🔄 추천 알고리즘

## 1. 감정 기반 분기 처리

### 행복 50% 이하

위로 모드(Comfort)

* 선호 가수 기반 음악 추천
* 익숙하고 편안한 장소 추천

### 행복 50% 초과

성장 모드(Challenge)

* 새로운 음악 추천
* 가보고 싶은 장소 추천

---

## 2. 추천 중복 방지

추천 콘텐츠의 다양성을 위해 중복 제거 로직을 적용하였습니다.

* 음악: 최근 14일 이내 추천 제외
* 장소: 최근 21일 이내 추천 제외

---

## 3. 실시간 추천 갱신

다음 정보가 변경되면 추천 결과를 즉시 갱신합니다.

* 일기 수정
* 감정 분석 결과 변경
* 설문 정보 수정

---

# 👨‍👩‍👧‍👦 팀 구성

| 이름  | 역할          | 담당 업무                                   |
| --- | ----------- | --------------------------------------- |
| 유연주 | Team Leader | 일기 작성, AI 감정 분석, 캘린더, 회원가입/로그인 |
| 박주한 | Member      | 통계 페이지, 감정 시각화, 콘텐츠 추천                  |
| 강동훈 | Member      | 설문 페이지, 설문 저장 및 수정, 모델 파인튜닝             |

---

# 📷 서비스 화면

## 회원가입 및 로그인 페이지
<img width="458" height="969" alt="image" src="https://github.com/user-attachments/assets/79c18375-56eb-4915-becf-6c0e652935ee" />
<img width="452" height="971" alt="image" src="https://github.com/user-attachments/assets/4bc14413-d594-4ef1-aaf6-e84c1a14de85" />


## 일기 페이지
<img width="463" height="984" alt="image" src="https://github.com/user-attachments/assets/def16946-16e6-4500-b85e-298a26c60c27" />
<img width="447" height="984" alt="image" src="https://github.com/user-attachments/assets/6fb4b16a-3dfc-45a0-9577-8143f4ea8e97" />


## 설문페이지 및 통계페이지
<img width="462" height="925" alt="image" src="https://github.com/user-attachments/assets/c30c9b65-8c11-4196-aed1-99e20db3f5c4" />
<img width="437" height="927" alt="image" src="https://github.com/user-attachments/assets/d0a2938f-a1ff-41f1-96c2-66cb60f5d553" />

# 📁 프로젝트 구조

```text
innernote-project
├── frontend
│   ├── public
│   ├── src
│   │   ├── pages
│   │   ├── components
│   │   ├── assets
│   │   └── router
│   ├── package.json
│   └── vite.config.js
│
├── backend
│   ├── app
│   │   ├── ai
│   │   ├── user
│   │   ├── diary
│   │   ├── emotion
│   │   ├── recommendation
│   │   ├── statistics
│   │   ├── survey
│   │   ├── core
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

---

# 🔗 Repository

GitHub

```bash
https://github.com/yooyeonjoo02/innernote-project
```
