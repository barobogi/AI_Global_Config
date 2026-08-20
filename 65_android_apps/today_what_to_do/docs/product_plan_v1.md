
# 오늘 뭐하지? — 공공데이터 기반 상황 맞춤형 장소·코스 추천 안드로이드 앱 기획서

> 문서 버전: v1.0  
> 작성 기준일: 2026-08-20  
> 목표: 실제 Google Play 배포를 전제로 한 MVP 및 상용화 설계  
> 플랫폼: Android 우선 / 이후 iOS·Web 확장  
> 프로젝트 성격: 공공데이터 + 지도/경로 API + 날씨 + AI 추천을 결합한 상황 기반 의사결정 서비스

---

## 0. 프로젝트 한 줄 정의

**“지금 내 상황에 맞춰, 오늘 갈 곳과 1~3시간짜리 실제 코스를 대신 골라주는 앱.”**

일반적인 장소 검색 앱은 사용자가 직접 검색하고 비교해야 한다.

`오늘 뭐하지?`는 사용자가 몇 가지 조건만 입력하면,

- 현재 위치 또는 출발지
- 동행자 유형
- 연령대
- 날짜/시간
- 이동수단
- 예산
- 실내/실외
- 선호/비선호
- 반려동물 동반 여부

를 바탕으로 **“지금 갈 만한 선택지”를 점수화하고, 이동 가능한 실제 코스까지 추천**한다.

핵심은 데이터를 많이 보여주는 것이 아니라 **결정을 줄여주는 것**이다.

---

# 1. 문제 정의

## 1.1 사용자가 겪는 문제

주말이나 외출 직전에 사용자는 다음을 동시에 고려해야 한다.

- 지금 날씨가 어떤가?
- 아이와 갈 수 있는가?
- 운영 중인가?
- 너무 멀지는 않은가?
- 차가 있는가?
- 주차가 가능한가?
- 입장료가 비싸지는 않은가?
- 비가 오면 대안이 있는가?
- 여러 장소를 어떤 순서로 가야 하는가?

현재 서비스들은 장소 검색에는 강하지만, 이 조건들을 종합하여 **“오늘 지금 가기 좋은 선택”**으로 압축하는 데는 한계가 있다.

## 1.2 해결책

사용자가 다음처럼 입력하도록 한다.

> “7살 아이와 오늘 오후 2시부터 5시까지 서울에서 놀고 싶어.  
> 차는 없고, 비가 올 것 같아. 총 3만 원 이내.”

앱은 다음을 자동 수행한다.

1. 현재/예상 날씨 확인
2. 관광·문화·체험 데이터 조회
3. 영업시간·휴무일 필터링
4. 이동수단 기준 접근성 계산
5. 거리·소요시간 계산
6. 예산 및 동행자 적합성 평가
7. 장소 후보를 점수화
8. 1~3개의 코스를 생성
9. 비가 심해질 경우 대체 장소까지 제안
10. 사용자가 저장/공유/길찾기를 바로 실행

---

# 2. 핵심 차별점

## 2.1 검색이 아니라 의사결정

### 기존
`“서울 어린이 체험” → 결과 300개`

### 오늘 뭐하지?
`“7살 / 비 / 3시간 / 대중교통 / 3만원” → 오늘 가능한 코스 3개`

## 2.2 데이터 결합

단일 데이터셋을 보여주는 앱이 아니라 다음을 결합한다.

```text
관광·문화 데이터
        +
날씨 데이터
        +
위치/거리 데이터
        +
운영시간/행사 데이터
        +
사용자 조건
        ↓
추천 엔진
        ↓
오늘 가능한 코스
```

## 2.3 AI는 “검색 엔진”이 아니라 “판단 계층”

AI에게 모든 데이터를 직접 맡기지 않는다.

- 사실 데이터: API/DB
- 필터링: 코드
- 점수 계산: 규칙 + 모델
- 자연어 설명: AI

이렇게 분리하여 환각과 잘못된 추천을 줄인다.

---

# 3. 1차 타깃 사용자

## Primary Persona A — 아이와 외출하는 보호자

- 30~40대
- 자녀 3~13세
- 주말 외출 결정 시간이 짧음
- 아이가 지루하지 않을 장소를 찾고 싶음
- 날씨/주차/운영시간을 중요하게 봄

## Persona B — 데이트/친구 외출

- 20~30대
- 당일 즉흥 외출
- “뭐하지?” 문제 해결
- 카페/관광/전시/체험 조합 선호

## Persona C — 반려동물 동반

- 반려견과 함께 외출
- 동반 가능 여부가 매우 중요
- 장소보다 “실제 들어갈 수 있는지”가 핵심

---

# 4. MVP 범위

처음부터 모든 기능을 만들지 않는다.

## MVP에서 반드시 제공

### 입력

- 현재 위치
- 이동수단: 도보 / 대중교통 / 자동차
- 동행: 혼자 / 연인 / 친구 / 아이 / 반려동물
- 예상 체류시간
- 예산
- 실내/실외 선호
- 날짜/시간

### 출력

1. 추천 장소 TOP 5
2. 추천 코스 TOP 3
3. 추천 이유
4. 예상 이동시간
5. 예상 총 소요시간
6. 예상 비용
7. 날씨 정보
8. 운영시간/휴무 정보
9. 지도 보기
10. 길찾기 연결
11. 저장
12. 공유

---

# 5. MVP 사용자 흐름

```text
[앱 실행]
    ↓
[현재 위치 허용]
    ↓
[“오늘 어디 갈까요?”]
    ↓
[동행자 선택]
    ↓
[시간/예산/이동수단]
    ↓
[실내/실외]
    ↓
[추천 생성]
    ↓
┌────────────────────┐
│ 추천 코스 A         │
│ 박물관 → 체험 → 식사 │
│ 2시간 40분          │
│ 예상비용 24,000원   │
│ 추천점수 94         │
└────────────────────┘
    ↓
[코스 상세]
    ↓
[지도/길찾기]
    ↓
[저장·공유]
```

---

# 6. 데이터 전략

## 6.1 1순위 공공데이터

### A. 한국관광공사 국문 관광정보 서비스

활용 대상:

- 관광지
- 문화시설
- 행사
- 숙박
- 위치 기반 검색
- 키워드 검색
- 이미지
- 반려동물 동반 여행 정보

공공데이터포털 설명상 전국 관광정보와 사진정보를 OpenAPI로 제공하고 모바일 앱·웹서비스 등에 활용할 수 있으며, 약 26만 건의 국내 관광 관련 정보를 제공한다.  
참고:
- https://www.data.go.kr/data/15101578/openapi.do

특히 `locationBasedList2`, `searchFestival2`, `detailCommon2`, `detailIntro2`, `detailPetTour2` 등을 MVP에서 활용한다.

### B. 한국관광공사 반려동물 동반여행 서비스

활용 대상:

- 반려동물 동반 관광지
- 숙소
- 음식점
- 쇼핑시설
- 반려동물 동반 조건
- 주의사항
- 이용 가능 시설
- 위치 기반 조회

현재 공공데이터포털 기준 무료이며 이용허락범위는 “제한 없음”으로 표시되어 있다. 운영단계는 심의승인이다.  
참고:
- https://www.data.go.kr/data/15135102/openapi.do

**중요:** 상용 서비스 출시 시에도 해당 시점의 API 이용약관/운영승인 상태를 다시 확인한다.

### C. 기상청 단기예보 조회서비스

활용 대상:

- 현재 기상
- 시간별 예보
- 강수량
- 기온
- 풍속
- 강수형태

공공데이터포털 기준 무료 REST API이며 실시간 업데이트, 개발계정 트래픽 10,000건, 운영계정은 활용사례 등록 시 확대 가능으로 안내되어 있다. 이용조건은 출처표시 공공저작물 제1유형이다.  
참고:
- https://www.data.go.kr/data/15084084/openapi.do

---

# 7. 데이터 사용 정책

상용 앱에서 가장 중요한 원칙:

## “공공데이터라고 해서 모든 데이터와 이미지가 자동으로 상업적 자유 이용 가능한 것은 아니다.”

특히 관광정보의 사진은 개별 권리 조건이 붙을 수 있다.

따라서 DB를 다음처럼 구분한다.

```text
[상용 사용 가능 확인]
    ├─ API 데이터
    ├─ 텍스트
    └─ 이미지
          ↓
[정책 테이블]
          ↓
commercial_use
attribution_required
image_use_restriction
source_url
last_verified_at
```

앱의 운영 DB에는 반드시 각 데이터의 출처와 정책 확인일을 저장한다.

---

# 8. 데이터 아키텍처

## 8.1 권장 구조

```text
Android App
     │
     ▼
Backend API
     │
 ┌───┼─────────────┐
 ▼   ▼             ▼
DB  Recommendation  Cache
     Engine
     │
 ┌───┼─────────────────────┐
 ▼   ▼         ▼           ▼
관광  날씨      지도/거리    사용자 DB
API   API       API
```

## 8.2 왜 Backend가 필요한가?

공공 API 키를 Android 앱 안에 직접 넣으면 앱 분석/역컴파일을 통해 노출될 수 있다.

따라서:

```text
Android
   ↓
내 서버
   ↓
공공 API
```

형태를 권장한다.

---

# 9. 추천 엔진 설계

## 9.1 1단계 — Hard Filter

조건에 맞지 않는 장소는 제거한다.

```python
if not is_open:
    reject()

if price > user_budget:
    reject()

if distance > max_distance:
    reject()

if user_with_pet and not pet_allowed:
    reject()

if user_prefers_indoor and venue.is_outdoor and rain_probability > 60:
    reject()
```

## 9.2 2단계 — Score

남은 장소에 점수를 부여한다.

예시:

```text
recommend_score =
  0.25 * condition_match
+ 0.20 * distance_score
+ 0.15 * weather_fit
+ 0.15 * time_fit
+ 0.10 * budget_fit
+ 0.10 * popularity
+ 0.05 * novelty
```

초기에는 규칙 기반으로 시작한다.

사용자가 쌓이면 개인화 추천으로 발전한다.

---

# 10. AI 역할

AI에게 다음을 맡긴다.

## 가능

- 추천 이유 자연어 생성
- 사용자 질문 해석
- 선호 조건 구조화
- 코스 설명
- 대체 일정 제안
- 사용자 리뷰 요약
- “아이와 가기 좋은 이유” 설명

## AI에게 맡기면 안 되는 것

- 영업 여부의 사실 판단
- 가격의 사실 판단
- 장소가 실제로 반려동물 동반 가능한지 임의 판단
- 날씨의 사실 판단
- 위치 좌표 생성

이런 정보는 **API/DB를 source of truth**로 한다.

---

# 11. 3AI 시스템 역할 분담

프로젝트에서 3개의 AI를 사용한다면 아래처럼 분리한다.

## AI-1: Product Planner

역할:

- 요구사항 해석
- 사용자 시나리오 생성
- 기능 우선순위
- UX 문구
- 실험 설계
- KPI 분석

입력:

```json
{
  "user_request": "...",
  "constraints": "...",
  "current_context": "..."
}
```

출력:

```json
{
  "intent": "family_outing",
  "duration_min": 180,
  "budget": 30000,
  "indoor_preference": true
}
```

---

## AI-2: Data/Recommendation Agent

역할:

- 후보 장소 데이터 조합
- 추천 근거 검증
- 조건 필터링 결과 설명
- 코스 조합 제안
- 데이터 품질 체크

단, 최종 사실값은 DB/API를 참조해야 한다.

권장 출력:

```json
{
  "recommendations": [
    {
      "place_id": "123",
      "score": 94,
      "reasons": [
        "비 예보에 적합한 실내 활동",
        "7세 아동 동반 조건과 잘 맞음",
        "현재 위치에서 대중교통 28분"
      ]
    }
  ]
}
```

---

## AI-3: QA / Safety / Fact Checker

역할:

- 추천 데이터 누락 점검
- API 데이터와 AI 설명 불일치 검사
- 운영시간/휴무일 모순 검사
- 상용화 금지 데이터 포함 여부 검사
- 위험한 추천 문구 차단

예:

```text
AI-2:
“오늘 오후 7시까지 운영합니다.”

AI-3:
실제 detailIntro 데이터:
“매주 월요일 휴무”

→ 현재 요일 확인 필요
→ 추천 설명 보류
```

이 구조는 AI가 스스로 사실을 만들어내는 문제를 줄이는 데 중요하다.

---

# 12. 3AI 전체 파이프라인

```text
사용자 입력
    ↓
AI-1
의도/조건 구조화
    ↓
Backend
데이터 조회
    ↓
Rule Engine
Hard Filter
    ↓
AI-2
추천 후보 설명 및 코스 생성
    ↓
AI-3
사실성/정책/안전 검증
    ↓
최종 JSON
    ↓
Android UI
```

---

# 13. Android 기술 스택

## 권장

### App

- Kotlin
- Jetpack Compose
- Navigation Compose
- ViewModel
- Kotlin Coroutines
- Retrofit 또는 Ktor Client
- Room
- DataStore
- WorkManager
- Firebase Analytics
- Firebase Crashlytics

### Backend

초기 추천:

- Python
- FastAPI
- PostgreSQL
- Redis
- Celery 또는 APScheduler

또는

- TypeScript
- NestJS
- PostgreSQL
- Redis

팀이 AI/데이터 작업에 익숙하면 Python FastAPI가 편하다.

---

# 14. DB 설계

## place

```sql
place_id
source
source_place_id
name
category
lat
lng
address
phone
homepage
description
price_min
price_max
indoor_outdoor
opening_hours
holiday
pet_allowed
image_url
source_policy
last_synced_at
```

## event

```sql
event_id
place_id
title
start_at
end_at
price
description
source
last_synced_at
```

## weather_cache

```sql
region_id
forecast_time
temperature
rain_probability
precipitation
weather_code
updated_at
```

## user_profile

```sql
user_id
age_group
travel_style
budget_range
mobility
companion_type
pet_type
preferred_indoor_outdoor
```

## recommendation_log

```sql
id
user_id
request_json
result_json
clicked_place_id
saved
route_started
feedback
created_at
```

---

# 15. API 설계

## POST /v1/recommendations

요청:

```json
{
  "lat": 37.5665,
  "lng": 126.9780,
  "date": "2026-08-20",
  "start_time": "14:00",
  "duration_minutes": 180,
  "budget": 30000,
  "transport": "transit",
  "companions": {
    "type": "child",
    "age": 7
  },
  "preference": {
    "indoor": true,
    "crowd": "low"
  }
}
```

응답:

```json
{
  "request_id": "req_123",
  "summary": "비 예보를 고려해 실내 체험형 코스를 추천합니다.",
  "recommendations": [
    {
      "rank": 1,
      "score": 94,
      "places": [
        {
          "place_id": "A001",
          "name": "장소 A",
          "stay_minutes": 90
        },
        {
          "place_id": "B002",
          "name": "장소 B",
          "stay_minutes": 60
        }
      ],
      "estimated_cost": 24000,
      "estimated_total_minutes": 165
    }
  ]
}
```

---

# 16. 지도/길찾기 전략

지도는 직접 지도 서비스를 개발하지 않는다.

MVP:

1. 위치 좌표를 앱에서 사용
2. 지도 SDK로 장소 표시
3. 외부 길찾기 앱 연결

후속 단계:

- 이동시간 API
- 대중교통 ETA
- 자동차 예상시간
- 도보 경로
- 복수 장소 TSP 최적화

를 붙인다.

**지도 사업자의 SDK/API와 상업적 이용조건은 실제 도입 시 해당 사업자의 최신 약관을 별도로 확인한다.**

---

# 17. 코스 생성 알고리즘

예:

```text
Candidate A: 박물관
Candidate B: 체험관
Candidate C: 카페
Candidate D: 공원
```

사용자가

```text
3시간
아이
비
대중교통
3만원
```

을 선택하면:

1. 실외 장소 감점
2. 비 영향 큰 장소 제거
3. 이동시간 계산
4. 영업시간 겹치는 조합 제거
5. 체류시간 합산
6. 비용 합산
7. 점수 계산
8. 가장 높은 조합 반환

---

# 18. 추천 점수 예시

```python
score = (
    condition_match * 0.25
    + distance_score * 0.20
    + weather_fit * 0.15
    + time_fit * 0.15
    + budget_fit * 0.10
    + popularity * 0.10
    + novelty * 0.05
)
```

각 값은 0~100으로 정규화한다.

초기에는 사람이 가중치를 조정한다.

장기적으로는 실제 클릭·저장·방문 데이터를 통해 학습한다.

---

# 19. 개인화 추천

사용자가 반복 사용할수록 다음 행동을 저장한다.

```text
조회
클릭
저장
공유
길찾기
실제 방문 추정
별점
추천 거절 이유
```

예를 들어:

```text
사용자 A
- 실내 72%
- 아이 체험 63%
- 이동 30분 이하 선호
- 1만원 이하 선호
- 카페 선호 높음
```

그러면 이후 추천에서 자동 반영한다.

---

# 20. 중요한 UX 기능

## “왜 이곳을 추천했나요?”

각 추천에는 근거를 보여준다.

예:

> ⭐ 추천점수 94  
> 비 예보라 실내 활동에 적합  
> 현재 위치에서 24분  
> 7세 아이 체험에 적합  
> 예산 3만원 안에서 가능

이 기능은 AI 서비스에 대한 신뢰를 크게 높인다.

---

# 21. “대안 바꾸기”

사용자가 추천을 거절하면 전체를 다시 검색하지 않는다.

예:

> “박물관 말고 더 활동적인 곳”

→ 해당 조건만 바꿔 재랭킹.

버튼 예시:

- 더 저렴하게
- 더 가까운 곳
- 덜 붐비는 곳
- 실내로
- 활동적인 곳
- 조용한 곳
- 아이가 좋아할 만한 곳
- 반려동물 가능

---

# 22. 날씨 대응 기능

핵심 기능으로 권장한다.

```text
맑음
→ 야외 가중치 ↑

비
→ 실내 가중치 ↑

폭염
→ 이동거리 ↓

강풍
→ 야외 활동 ↓
```

예:

> “오후 4시 이후 강수 가능성이 높아 마지막 코스를 실내 장소로 바꿨어요.”

단, 이 문장은 날씨 API 값으로 검증된 경우에만 표시한다.

---

# 23. 상용화 수익모델

## 1단계 — 무료 + 광고

- 일반 추천 무료
- 비강압적 네이티브 광고
- 장소 상세의 스폰서 슬롯

## 2단계 — 프리미엄

월 구독:

- AI 고급 코스
- 취향 학습
- 가족 프로필
- 여행 일정 저장
- 광고 제거
- 장거리 여행 최적화

## 3단계 — 제휴

- 관광시설
- 체험시설
- 식당
- 카페
- 숙박
- 렌터카

예약/쿠폰/제휴 링크 수익.

## 중요한 원칙

**추천 결과를 돈을 많이 내는 업체에 유리하게 조작하지 않는다.**

광고/제휴 추천은 “광고”, “제휴”로 명확히 표시한다.

---

# 24. KPI

## 초기

- 설치 수
- 가입 전환율
- 위치 권한 허용률
- 추천 생성률
- 추천 클릭률

## 핵심 KPI

### Recommendation-to-Action Rate

```text
추천을 받은 사용자 중
저장/길찾기/공유 등 행동을 한 비율
```

### Repeat Recommendation Rate

```text
7일 내 두 번째 추천을 요청한 사용자 비율
```

### Recommendation Satisfaction

앱에 간단히 질문한다.

> “이 추천이 도움이 되었나요?”

👍 / 👎

---

# 25. MVP 출시 조건

다음이 모두 되면 베타 출시한다.

- [ ] 회원가입 또는 익명 사용자 지원
- [ ] 위치 권한 처리
- [ ] 관광 데이터 수집
- [ ] 날씨 데이터 수집
- [ ] 데이터 정규화
- [ ] 장소 검색
- [ ] 추천 점수 계산
- [ ] 코스 생성
- [ ] 지도 표시
- [ ] 길찾기 연결
- [ ] 추천 이유 표시
- [ ] 저장
- [ ] 공유
- [ ] 오류 처리
- [ ] API 키 서버 보관
- [ ] 개인정보처리방침
- [ ] 이용약관
- [ ] 공공데이터 출처 표시
- [ ] 상용 이용 정책 확인
- [ ] Crashlytics
- [ ] Analytics
- [ ] Play Console 등록 준비

---

# 26. 개발 단계

## Phase 0 — 1주

### 검증

- 사용할 API 신청
- 상용 이용조건 확인
- 응답 데이터 구조 분석
- 실제 데이터 100~1,000건 확보
- 주요 경쟁 앱 조사

산출물:

```text
data_dictionary.md
api_inventory.md
legal_checklist.md
```

---

## Phase 1 — 1~2주

### Backend Prototype

구현:

- 관광 API 연결
- 날씨 API 연결
- DB 저장
- 캐시
- 장소 검색 API

산출물:

```text
GET /places
GET /weather
GET /events
```

---

## Phase 2 — 2주

### 추천엔진

구현:

- Hard Filter
- 거리 계산
- 운영시간 필터
- 날씨 적합도
- 예산 점수
- 기본 추천

이 단계에서는 AI 없이도 동작해야 한다.

---

## Phase 3 — 2~3주

### Android MVP

화면:

1. Splash
2. Home
3. 조건 입력
4. 추천 결과
5. 추천 상세
6. 지도
7. 저장
8. 마이페이지

---

## Phase 4 — 1~2주

### AI

AI-1:
자연어 조건 이해

AI-2:
코스 설명/대안 생성

AI-3:
팩트 검증

---

## Phase 5 — 베타

테스터 30~100명을 모집한다.

테스트 질문:

- 추천이 실제로 유용했는가?
- 정보가 맞았는가?
- 추천 시간이 합리적인가?
- 코스가 실제로 이동 가능한가?
- 어떤 조건을 가장 많이 쓰는가?

---

# 27. 테스트 전략

## 단위 테스트

- 가격 필터
- 운영시간
- 거리
- 날씨
- 반려동물 조건

## 통합 테스트

```text
관광 API
→ DB
→ 추천엔진
→ AI
→ Android
```

## E2E 테스트

시나리오:

> 7세 아이 / 서울 / 오늘 / 3시간 / 3만원 / 대중교통 / 비

기대 결과:

- 실내 장소 중심
- 운영 중인 장소만
- 3시간 내 코스
- 3만원 이하
- 이동시간 포함

---

# 28. AI 안전장치

AI 결과에는 반드시 `evidence`를 붙인다.

```json
{
  "claim": "현재 영업 중입니다.",
  "evidence": {
    "source": "KorService2",
    "field": "usetime",
    "last_updated": "2026-08-20T09:10:00+09:00"
  }
}
```

AI가 근거 없는 사실을 생성하면 사용자에게 노출하지 않는다.

---

# 29. 데이터 업데이트

공공 API는 항상 변경될 수 있다.

따라서:

```text
API Collector
    ↓
Raw Data
    ↓
Normalizer
    ↓
Validator
    ↓
PostgreSQL
    ↓
Recommendation DB
```

형태로 만든다.

주기:

- 실시간 데이터: 캐시 수분~수십분
- 관광 기본정보: 하루 1회 또는 동기화 목록 활용
- 행사정보: 하루 수회
- 이미지: URL/메타데이터 정책 확인 후 처리

---

# 30. 장애 대응

API가 죽었다고 앱 전체가 죽으면 안 된다.

```text
Primary API
   ↓ 실패
Cache
   ↓ 없음
Fallback API/기본 DB
   ↓
“최신 정보 확인 필요” 표시
```

특히 영업시간/행사 시간과 같이 중요한 정보는 오래된 캐시를 사실처럼 표시하지 않는다.

---

# 31. 개인정보

MVP에서 최대한 적게 수집한다.

필수:

- 위치
- 추천 요청 조건

선택:

- 저장한 장소
- 선호
- 사용자 계정

가능하면 정확한 위치를 서버에 지속 저장하지 않고, 추천 요청 시만 전달한다.

---

# 32. Play Store 출시 체크리스트

- [ ] 앱 이름 상표 검토
- [ ] 패키지명 확보
- [ ] 개인정보처리방침
- [ ] 이용약관
- [ ] 위치 권한 설명
- [ ] 알림 권한 설명
- [ ] 광고 표시
- [ ] 데이터 수집/공유 선언
- [ ] 계정 삭제 절차
- [ ] 공공데이터 출처
- [ ] API 약관 확인
- [ ] 이미지 저작권 확인
- [ ] 스크린샷
- [ ] 앱 아이콘
- [ ] 콘텐츠 등급
- [ ] 내부/비공개/공개 테스트
- [ ] Crashlytics 확인

---

# 33. 추천 화면 예시

```text
┌─────────────────────────┐
│ 📍 서울 마포구          │
│                         │
│ 오늘 뭐하지?            │
│                         │
│ 👧 7살 아이              │
│ ☔ 비                   │
│ 🚌 대중교통              │
│ ⏰ 14:00 ~ 17:00         │
│ 💰 30,000원              │
│                         │
│      [추천받기]          │
└─────────────────────────┘
```

결과:

```text
┌─────────────────────────┐
│ 🥇 추천 94점             │
│                         │
│ 실내 체험 + 카페 코스    │
│                         │
│ 체험관 → 어린이 전시     │
│ → 카페                   │
│                         │
│ 🕐 2시간 42분            │
│ 💰 약 24,000원           │
│ 🚌 이동 31분             │
│ ☔ 비 적합도 ★★★★★       │
│                         │
│ “비 예보를 고려해       │
│ 실내 중심으로 구성했어요.”│
│                         │
│ [지도] [길찾기] [저장]   │
└─────────────────────────┘
```

---

# 34. 브랜드 방향

후보:

- 오늘 뭐하지?
- 어디갈까?
- 지금 갈까?
- 오늘한코스
- 딱좋아
- 여기어때?와 혼동되지 않는 독자 브랜드 필요

개인적으로는 초기 브랜드로

## `오늘뭐하지`

를 추천한다.

슬로건:

> **“검색 말고, 오늘의 답.”**

또는

> **“지금 내 상황에 딱 맞는 곳.”**

---

# 35. 장기 확장

## 1차

가족/아이 중심

## 2차

데이트

## 3차

반려동물

## 4차

국내 여행

## 5차

AI 여행 비서

최종적으로는:

```text
“이번 토요일 아이와 부산에 갈 거야.
10시부터 18시까지,
차로 이동하고,
예산은 15만원,
비 올 가능성이 있으면 실내 위주로 해줘.”

                ↓

AI 여행 플래너

                ↓

교통
날씨
관광
식사
숙박
행사
주차
예산
운영시간

                ↓

실행 가능한 일정
```

으로 확대할 수 있다.

---

# 36. 중요한 사업적 판단

이 앱의 경쟁력은 “데이터가 많다”가 아니다.

## 경쟁력 = 개인 상황을 얼마나 정확하게 해석하여 실행 가능한 선택으로 바꾸느냐

따라서 초반에는 AI 모델의 크기보다 아래 요소가 중요하다.

1. 데이터 품질
2. 운영시간 정확성
3. 거리 계산
4. 날씨 반영
5. 추천 이유
6. 빠른 응답
7. 실제 사용 후 피드백

---

# 37. 첫 번째 개발 목표

처음부터 거대한 플랫폼을 만들지 않는다.

## Sprint 1 목표

### 사용자가

> “7살 아이와 오늘 3시간 동안 서울에서 놀 곳을 찾아줘. 비가 와.”

라고 입력했을 때,

### 앱이

> “실내 중심 추천 3개”

를 **10초 이내**에 보여주는 것.

그리고 각 추천에

- 왜 추천했는지
- 지금 운영하는지
- 얼마나 걸리는지
- 얼마가 필요한지
- 지도
- 길찾기

가 붙어 있으면 MVP 성공이다.

---

# 38. 개발 폴더 구조

```text
today-what-to-do/
│
├── docs/
│   ├── product_requirements.md
│   ├── api_inventory.md
│   ├── data_dictionary.md
│   ├── legal_checklist.md
│   └── ai_architecture.md
│
├── android/
│   ├── app/
│   ├── core/
│   ├── data/
│   ├── domain/
│   ├── feature-home/
│   ├── feature-recommendation/
│   ├── feature-map/
│   └── feature-profile/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── recommend/
│   │   └── integrations/
│   └── tests/
│
├── ai/
│   ├── prompts/
│   ├── planner/
│   ├── recommender/
│   └── verifier/
│
└── infra/
    ├── docker/
    └── deploy/
```

---

# 39. 3AI에게 작업시키기 위한 기본 지시

## AI-1 Product Planner Prompt

```text
너는 이 프로젝트의 Product Planner다.

제품:
“오늘 뭐하지?”
공공데이터와 AI를 활용하여 사용자의 현재 상황에 맞는
장소와 코스를 추천하는 Android 앱이다.

원칙:
1. 사용자의 의도를 구조화한다.
2. 불필요한 기능을 추가하지 않는다.
3. MVP를 우선한다.
4. 기능별 사용자 가치와 개발 난이도를 함께 판단한다.
5. 모든 요구사항을 JSON 형태로 구조화할 수 있어야 한다.

현재 요청:
{USER_REQUEST}

출력:
- intent
- constraints
- required_features
- optional_features
- acceptance_criteria
```

---

## AI-2 Recommendation Agent Prompt

```text
너는 추천 시스템의 코스 설계 AI다.

중요:
모든 사실 정보는 전달받은 DB/API 데이터만 사용한다.
모르는 정보는 추측하지 않는다.

입력:
- 사용자 조건
- 후보 장소 목록
- 날씨
- 거리
- 운영시간
- 비용

작업:
1. 후보를 비교한다.
2. 조건에 맞는 코스를 구성한다.
3. 추천 이유를 만든다.
4. 데이터에 없는 사실을 만들지 않는다.

출력은 JSON으로 한다.
```

---

## AI-3 Fact Checker Prompt

```text
너는 QA 및 Fact Checker다.

목표:
AI 추천 결과가 원본 데이터와 일치하는지 확인한다.

검사:
- 운영시간
- 휴무
- 가격
- 위치
- 반려동물 가능 여부
- 날씨
- 추천 시간
- 데이터 최신성
- 상용 이용 정책

불일치가 하나라도 있으면
VERIFIED=false를 반환한다.

출력:
{
  "verified": true,
  "issues": [],
  "warnings": []
}
```

---

# 40. 다음 실제 작업 순서

## 반드시 이 순서대로 진행

### Step 1
공공데이터 API 발급

- 한국관광공사 국문 관광정보
- 반려동물 동반여행
- 기상청 단기예보

### Step 2
API 응답을 실제로 수집

목표:

```text
장소 1,000건+
행사 100건+
날씨 데이터
```

### Step 3
데이터 정규화

### Step 4
추천 엔진을 AI 없이 개발

### Step 5
Android 기본 UI 개발

### Step 6
지도/길찾기 연결

### Step 7
AI-1/2/3 연결

### Step 8
30명 이상 베타 테스트

### Step 9
추천 정확도 개선

### Step 10
Google Play 출시

---

# 41. Definition of Done

MVP는 다음 조건을 충족하면 “완료”로 본다.

```text
[사용자]
“현재 위치에서
7살 아이와
비 오는 날
3시간
3만원 이하로
갈 곳을 찾아줘”

        ↓

[앱]

1. 날씨 확인
2. 관광 데이터 조회
3. 운영시간 확인
4. 위치/거리 계산
5. 조건 필터
6. 점수 계산
7. 코스 생성
8. AI 추천 설명
9. QA 검증

        ↓

[결과]

추천 코스 3개
+
추천 이유
+
예상 비용
+
예상 시간
+
지도
+
길찾기
```

이 전체 흐름이 실제 단말에서 정상 작동하면 MVP 완료다.

---

# 42. 최종 제품 비전

`오늘 뭐하지?`는 단순한 관광지 검색 앱으로 시작하지 않는다.

**“공공데이터를 사람이 이해할 수 있는 선택으로 바꾸는 AI 생활 서비스”**를 목표로 한다.

첫 제품은 외출 추천이지만, 동일한 기술로 이후 다음 영역으로 확장할 수 있다.

```text
오늘 뭐하지?
    ↓
오늘 어디 가지?
    ↓
이번 주말 뭐 하지?
    ↓
여행 어떻게 가지?
    ↓
내 상황에서 가장 좋은 선택은?
```

핵심 제품 철학:

> **데이터는 보여주고, AI는 설명하고, 사용자는 쉽게 결정한다.**

---



# 부록 A. 원본 영상 및 공공데이터/API 접근 경로

## A-1. 원본 영상

- YouTube 원본: https://youtu.be/Ifq0Yt7Thzc?si=EE18E-6oW1iKd6vE
- 영상 제목: **정부가 공짜로 푸는 데이터 11,915개, 뭘 할 수 있는지 직접 만들어봤습니다**
- 용도: 본 프로젝트의 문제의식과 공공데이터 활용 아이디어를 참고하는 원본 자료

## A-2. 공공데이터포털 메인

- 공공데이터포털: https://www.data.go.kr/

### API를 찾는 기본 경로

```text
공공데이터포털(data.go.kr)
→ 데이터찾기
→ 데이터목록
→ 검색어 입력
→ 데이터 상세페이지
→ [오픈API] 탭 확인
→ 활용신청
→ 인증키/서비스키 발급
→ 상세기능/요청주소 확인
→ 참고문서(활용가이드) 다운로드
```

### 검색할 때 우선 확인할 항목

1. **API 유형**: REST인지 확인
2. **데이터포맷**: JSON 사용 가능 여부 확인
3. **활용신청**: 개발계정 신청 가능 여부
4. **신청가능 트래픽**: 개발/운영계정 제한 확인
5. **업데이트 주기**: 실시간/일간/주간 등 확인
6. **이용허락범위**: 상용 이용 가능 여부와 출처표시 조건 확인
7. **참고문서**: API 활용가이드 다운로드
8. **요청주소**: Base URL과 endpoint 확인
9. **요청변수**: 필수 파라미터와 인증키 위치 확인
10. **출력결과**: 실제 JSON 필드 구조 확인

---

## A-3. 1순위 데이터 — 한국관광공사 국문 관광정보 서비스

### 공공데이터포털 위치

https://www.data.go.kr/data/15101578/openapi.do

### 포털에서 보는 위치

```text
공공데이터포털
→ 검색창
→ “한국관광공사 국문 관광정보 서비스” 검색
→ 한국관광공사_국문 관광정보 서비스_GW
→ [오픈API 상세]
→ [활용신청]
```

공공데이터포털 페이지에는 모바일 앱, 웹서비스 등의 매체에서 활용할 수 있다고 안내되어 있으며, 지역기반·위치기반 관광정보, 키워드 검색, 행사, 숙박, 반려동물 동반여행 등의 API 기능이 제공된다. citeturn743057search2

### MVP에서 우선 사용할 endpoint

- `areaCode2` — 지역코드 조회
- `areaBasedList2` — 지역기반 관광정보 조회
- `locationBasedList2` — 현재 위치 기반 관광정보 조회
- `searchKeyword2` — 키워드 검색
- `searchFestival2` — 행사정보 조회
- `detailCommon2` — 공통 상세정보
- `detailIntro2` — 소개정보
- `detailImage2` — 이미지정보
- `detailPetTour2` — 반려동물 동반 정보

### 구현 시 데이터 흐름

```text
Android 위치
   ↓
Backend
   ↓
locationBasedList2
   ↓
거리/카테고리/운영조건 필터
   ↓
detailCommon2 + detailIntro2
   ↓
추천 DB
```

### 이미지 주의

관광정보 API의 사진은 데이터 본문과 동일하게 취급하면 안 된다. 공공데이터포털 페이지에 이미지별 이용 조건이 별도로 안내되어 있으므로 상용 앱에서는 **이미지마다 이용 가능 범위와 출처 조건을 확인한 뒤 사용**한다. citeturn743057search2

---

## A-4. 2순위 데이터 — 한국관광공사 반려동물 동반여행 서비스

### 공공데이터포털 위치

https://www.data.go.kr/data/15135102/openapi.do

### 포털에서 보는 위치

```text
공공데이터포털
→ 검색
→ “한국관광공사 반려동물 동반여행 서비스”
→ 오픈API 상세
→ 활용신청
→ OpenAPI 명세 확인
→ 참고문서(활용매뉴얼) 다운로드
```

이 API는 반려동물 동반 관광지·숙소·음식점·쇼핑시설과 운영시간, 휴무일, 동반 조건 등의 상세정보를 제공하며 위치기반 조회도 지원한다. 공공데이터포털 현재 페이지에는 무료, 개발계정 1,000건, 운영계정은 활용사례 등록 시 트래픽 증가 가능, 이용허락범위 제한 없음으로 표시되어 있다. 실제 상용화 전에는 최신 조건을 다시 확인한다. citeturn743057search0

### Base URL

```text
https://apis.data.go.kr/B551011/KorPetTourService2
```

### MVP 우선 endpoint

- `/locationBasedList2`
- `/areaBasedList2`
- `/detailPetTour2`
- `/detailCommon2`
- `/detailIntro2`
- `/detailImage2`

### 앱 기능 연결

```text
사용자 “강아지와 갈 곳”
          ↓
반려동물 조건 ON
          ↓
KorPetTourService2
          ↓
동반 가능 조건 필터
          ↓
날씨 + 거리 + 영업시간 결합
          ↓
추천
```

---

## A-5. 3순위 데이터 — 기상청 단기예보 조회서비스

### 공공데이터포털 위치

https://www.data.go.kr/data/15084084/openapi.do

### 포털에서 보는 위치

```text
공공데이터포털
→ 검색
→ “기상청 단기예보 조회서비스”
→ 오픈API 상세
→ 활용신청
→ 참고문서
→ 상세기능
→ 요청주소/요청변수 확인
```

기상청 단기예보 서비스는 초단기실황, 초단기예보, 단기예보를 제공하며 REST/JSON+XML 방식이다. 공공데이터포털 현재 페이지 기준 무료이며 개발계정 트래픽은 10,000건, 운영계정은 활용사례 등록 시 증가 가능하고, 이용조건은 출처표시 공공저작물 제1유형으로 표시되어 있다. citeturn743057search1turn743057search3

### Base URL

```text
http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0
```

### MVP 우선 endpoint

- `/getUltraSrtNcst` — 초단기실황
- `/getUltraSrtFcst` — 초단기예보
- `/getVilageFcst` — 단기예보
- `/getVilageFcst` 계열 요청은 발표시각(base_time), 예보 격자(nx, ny) 등을 확인해야 한다.

### 현재 위치 → 기상 데이터 변환

기상청 단기예보는 위경도 그대로 요청하는 방식이 아니라 예보 격자 `nx`, `ny`를 사용한다.
따라서 다음 변환 계층을 Backend에 둔다.

```text
Android GPS
(lat, lng)
   ↓
격자 변환 함수
   ↓
(nx, ny)
   ↓
기상청 API
   ↓
날씨 JSON
```

---

## A-6. API 인증키/서비스키를 가져오는 실제 위치

### 공통 절차

```text
1. data.go.kr 로그인
2. 원하는 OpenAPI 상세페이지 접속
3. [활용신청] 클릭
4. 개발계정 신청
5. 활용목적 입력
6. 승인/신청 완료 확인
7. 개인 마이페이지/활용신청 현황 이동
8. 발급된 인증키(ServiceKey) 확인
```

### 개발환경에서의 원칙

인증키를 Android APK에 직접 넣지 않는다.

```text
❌ Android 앱
   └── 공공API Key

✅ Android
   ↓
내 Backend
   ↓
환경변수/Secret Manager
   ↓
공공API Key
   ↓
공공데이터 API
```

### 권장 환경변수

```env
KTO_SERVICE_KEY=...
KTO_PET_SERVICE_KEY=...
KMA_SERVICE_KEY=...
```

실제 배포에서는 `.env` 파일을 저장소에 커밋하지 않고 Cloud Secret Manager, GitHub Actions Secrets 또는 배포 플랫폼의 Secret 기능을 사용한다.

---

## A-7. API 상세페이지에서 3AI가 반드시 찾아야 할 것

3AI가 새로운 공공데이터를 추가할 때는 반드시 다음 항목을 추출한다.

```json
{
  "dataset_name": "",
  "provider": "",
  "portal_url": "",
  "api_type": "REST",
  "base_url": "",
  "format": ["JSON"],
  "auth": "ServiceKey",
  "endpoints": [],
  "required_parameters": [],
  "optional_parameters": [],
  "traffic_limit_dev": 0,
  "traffic_limit_prod": 0,
  "update_cycle": "",
  "license": "",
  "commercial_use": "VERIFY",
  "attribution_required": true,
  "reference_document": "",
  "last_verified_at": ""
}
```

### 특히 `commercial_use`는 자동으로 true로 판단하지 않는다.

데이터의 상업적 이용 가능 여부는 **공공데이터라는 사실만으로 결정하지 않고 해당 데이터셋의 이용허락범위·개별 콘텐츠 권리·참고문서·제공기관 약관을 확인**한다.

---

## A-8. 3AI 데이터 발굴 프로토콜

### AI-1 — Data Scout

사용자의 새 기능 요청을 받으면:

```text
1. data.go.kr 검색
2. 후보 API 3개 이상 수집
3. 상세페이지의 이용조건 확인
4. Base URL/endpoint 확인
5. 참고문서 다운로드 위치 기록
6. 실제 API 응답 필드 확인
7. 상용 이용 가능 여부를 별도 검토
```

### AI-2 — Integration Engineer

```text
1. API client 작성
2. 인증키를 환경변수로 연결
3. JSON schema 정의
4. DB 모델 변환
5. 캐싱
6. 오류/timeout/retry 처리
7. 기존 추천엔진과 연결
```

### AI-3 — Compliance & QA

```text
1. 라이선스 확인
2. 출처표시 필요 여부 확인
3. 이미지 권리 확인
4. 데이터 최신성 확인
5. API 제한 확인
6. AI가 사실을 임의 생성했는지 확인
```

---

## A-9. API 호출 샘플 작성 위치

각 API를 프로젝트에 추가할 때 다음 파일을 만든다.

```text
docs/api/
├── kto_tourism.md
├── kto_pet_tourism.md
├── kma_weather.md
└── api_policy_matrix.md

backend/app/integrations/
├── kto_client.py
├── kto_pet_client.py
└── kma_client.py
```

각 `docs/api/*.md`에는 최소한 다음을 넣는다.

```text
- 공공데이터포털 URL
- Base URL
- 활용신청 위치
- 인증키 발급 방식
- Endpoint 목록
- 필수 파라미터
- 실제 요청 예시
- 실제 응답 예시
- 우리 DB 필드 매핑
- 트래픽 제한
- 업데이트 주기
- 라이선스/출처표시
- 상용화 검토일
```

---

## A-10. 프로젝트의 공식 참고 링크 목록

| 구분 | 링크 | 용도 |
|---|---|---|
| 원본 영상 | https://youtu.be/Ifq0Yt7Thzc?si=EE18E-6oW1iKd6vE | 공공데이터 활용 아이디어 참고 |
| 공공데이터포털 | https://www.data.go.kr/ | 전체 데이터 검색/활용신청 |
| 관광정보 API | https://www.data.go.kr/data/15101578/openapi.do | 관광지·행사·위치·상세정보 |
| 반려동물 API | https://www.data.go.kr/data/15135102/openapi.do | 반려동물 동반 장소 |
| 기상청 단기예보 | https://www.data.go.kr/data/15084084/openapi.do | 현재/예보 날씨 |

---

## A-11. 출시 전 필수 재검증

문서에 기재된 API 정보는 **2026-08-20 기준 공식 공개 페이지를 확인한 것**이다. 개발기간이 길어질 경우 다음 항목은 출시 직전에 다시 확인한다.

- [ ] API endpoint가 변경되지 않았는가?
- [ ] 서비스키 발급 방식이 변경되지 않았는가?
- [ ] 개발/운영 트래픽 제한이 변경되지 않았는가?
- [ ] 이용허락범위가 변경되지 않았는가?
- [ ] 참고문서 버전이 바뀌지 않았는가?
- [ ] 이미지의 개별 이용조건을 확인했는가?
- [ ] 상용 서비스 운영단계 승인/신청이 필요한가?
- [ ] 출처표시 문구를 앱에 넣었는가?

**원칙: API 문서의 현재 상태를 기준으로 구현하고, 출시 직전 공식 페이지를 재검증한다.**


# 43. 현재 확인한 공식 데이터 출처

- 한국관광공사 국문 관광정보 서비스  
  https://www.data.go.kr/data/15101578/openapi.do

- 한국관광공사 반려동물 동반여행 서비스  
  https://www.data.go.kr/data/15135102/openapi.do

- 기상청 단기예보 조회서비스  
  https://www.data.go.kr/data/15084084/openapi.do

위 정보와 이용조건은 2026-08-20 기준 공개 페이지를 확인한 내용을 바탕으로 정리했다. 실제 상용 출시 전에는 각 API의 최신 이용약관·운영승인·트래픽 정책·데이터별 저작권/공공누리 조건을 다시 확인한다.

---

# 44. 가장 먼저 만들 기능 10개

1. 위치 기반 추천
2. 동행자 선택
3. 시간 입력
4. 예산 입력
5. 실내/실외
6. 날씨 연동
7. 장소 필터링
8. 코스 점수화
9. 추천 이유 AI 생성
10. 지도/길찾기

**이 10개를 완성하면 “오늘 뭐하지?”는 단순 아이디어가 아니라 실제 베타 테스트 가능한 제품이 된다.**
