# 주차 어디가? — 상용화 확장 기획안 V2

## 0. 문서 목적

기존 「주차 어디가?」 기획의 핵심인 **공공데이터 기반 AI 주차 의사결정/추천**을 유지하면서, 상용 서비스 출시를 위한 제품/기술/데이터/보안/운영 로드맵을 구체화한다.

기존 기획에서 정의한 핵심 흐름:

```text
공공데이터
→ 후보 주차장
→ Hard Filter
→ 추천 점수
→ AI 추천 설명
→ Fact Checker
→ 사용자
```

을 다음 구조로 확장한다.

```text
공공데이터 + 제휴 API + 사용자 현장 데이터
→ 수집/정규화
→ 데이터 품질 엔진
→ 주차 성공확률
→ 추천/Plan B
→ AI 설명
→ Android
→ 실제 성공/실패 피드백
→ 다시 데이터 품질/모델 개선
```

---

# 1. 제품 포지셔닝

## 한 문장

> **주차장을 찾는 앱이 아니라, 지금 실제로 주차에 성공할 가능성이 높은 곳을 추천하는 앱.**

경쟁 서비스가 검색·예약·할인·결제·실시간 현황을 제공하더라도, 「주차 어디가?」는 **의사결정의 신뢰성**을 중심으로 차별화한다.

---

# 2. 상용화 핵심 문제

사용자가 겪는 가장 중요한 실패는 다음이다.

1. 앱에서는 가능하지만 현장은 만차
2. 앱 요금과 실제 요금이 다름
3. 주차장 좌표와 차량 입구가 다름
4. 구매한 주차권을 현장 상황 때문에 제대로 사용하지 못함
5. 어느 주차장이 최적인지 직접 비교해야 함
6. 1순위 주차장 실패 시 대안이 없음
7. 데이터가 언제 갱신됐는지 알기 어려움

따라서 제품의 핵심은 **정보량 증가가 아니라 실패 감소**다.

---

# 3. Killer Feature

## 3.1 Parking Success Probability

예:

```text
A 주차장
주차 성공 가능성 92%
데이터 신뢰도 95%
예상비용 6,000원
도보 5분
```

주의:

> 예측값이며 실제 주차를 보장하지 않는다.

## 3.2 Data Confidence

```text
🟢 매우 신뢰
마지막 확인 2분 전
공식 실시간 데이터
최근 사용자 신고 없음
```

## 3.3 Plan B

```text
PLAN A  A 주차장 92%
PLAN B  B 주차장 84%
PLAN C  C 주차장 58%
```

---

# 4. 추천 엔진 V2

## 입력

- 목적지
- 예상 주차시간
- 현재 위치
- 최대 도보거리
- 예산
- 가격 선호
- 거리 선호
- 성공 가능성 선호
- 접근성
- EV/충전 필요 여부

## 데이터

- 운영 여부
- 주차면
- 실시간 잔여면
- 요금
- 거리
- 도보시간
- 차량 입구
- 데이터 최신성
- 사용자 신고
- 과거 성공/실패
- 시간/요일 패턴

## 출력

```text
score
success_probability
confidence
reasons
risks
plan_b
```

---

# 5. 데이터 품질 엔진

같은 주차장 정보라도 원천과 최신성에 따라 신뢰도가 다르다.

권장 내부 모델:

```text
freshness
source_reliability
consistency
user_verification
field_completeness
```

사용자에게는 숫자를 그대로 강요하지 않고:

```text
매우 신뢰
신뢰
확인 필요
오래된 정보
```

로 보여준다.

---

# 6. 현장 신고

3초 내 신고가 목표다.

```text
주차 성공?
[성공] [실패]

실패 이유
[만차]
[입구 문제]
[요금 불일치]
[운영 안 함]
[주차권 문제]
[기타]
```

신고는 리뷰 시스템이 아니라 **데이터 품질 이벤트**로 취급한다.

---

# 7. 차량 입구 데이터

주차장 중심 좌표와 차량 입구를 분리한다.

```text
parking_center
car_entrance
pedestrian_entrance
exit
elevator
```

최종 목적은:

> “주차장까지”가 아니라 **“차량 입구까지” 안내**다.

---

# 8. Preflight Check

주차권/예약/길찾기 직전에 마지막 검증:

```text
주차장
사용시간
현재 상태
최근 만차 신고
운영시간
예상 요금
데이터 최신성
```

이상이 없을 때만 구매/이동을 권한다.

---

# 9. 주차 Journey

```text
목적지 입력
↓
추천
↓
Plan A/B
↓
출발 전 재검증
↓
차량 입구 안내
↓
입차
↓
주차 타이머
↓
출차 알림
↓
실제 결제금액
↓
성공/실패 피드백
```

이 전체 흐름을 하나의 제품 경험으로 만든다.

---

# 10. Android 아키텍처

Jetpack Compose 공식 권장 패턴에 맞춰 UDF, 상태 홀더/ViewModel, Repository 계층을 사용한다.

```text
UI
↓
ViewModel
↓
Use Case
↓
Repository
↓
Remote / Local
```

UI에는 비즈니스 로직을 넣지 않는다.

---

# 11. Backend 아키텍처

```text
API
├── parking
├── feedback
├── auth
├── user
├── navigation
└── reservation

Service
├── recommendation
├── data_quality
├── prediction
├── pricing
├── entrance
└── notification

Repository
├── parking
├── feedback
└── user
```

---

# 12. Data Ingestion

```text
공공 API
제휴 API
사용자 신고
      ↓
Adapter
      ↓
Normalizer
      ↓
Validator
      ↓
Canonical Parking Model
      ↓
PostgreSQL
      ↓
Redis
```

API 공급자가 바뀌어도 추천엔진이 영향을 받지 않도록 한다.

---

# 13. 공공데이터 사용 원칙

공공 API는 공식 명세와 이용조건을 기준으로 구현한다.

확인해야 하는 항목:

- 인증키
- 호출 URL
- 요청 변수
- 응답 필드
- 업데이트 주기
- 상업적 이용
- 출처표시
- 캐싱
- 저장
- 재배포
- 호출량 제한
- 장애 대응

실제 명세 확인 전 필드를 임의로 확정하지 않는다.

---

# 14. 보안

## API Key

```text
Android X
Git X
로그 X

Secret Manager / Environment O
Backend O
```

## 개인정보

- 최소수집
- 목적 달성 후 삭제/비식별화
- 차량번호 암호화/마스킹
- 위치정보 최소 저장
- 로그 정밀위치 금지

## AI

AI는 가격/운영/잔여면을 생성하지 않는다.

```text
원천 데이터
↓
계산
↓
추천
↓
AI 설명
```

---

# 15. 장애 대응

실시간 API 장애 시:

```text
실시간 API
↓ 장애
최근 정상 데이터
↓
사용자에게
“마지막 확인 12분 전”
```

으로 보여준다.

“실시간인 척” 하지 않는다.

---

# 16. KPI

## 제품

- 추천 후 길찾기 전환율
- 추천 후 실제 주차 성공률
- Plan B 사용률
- 현장 신고율

## 데이터

- Data Freshness
- Data Accuracy
- Field Completeness
- Incident Resolution Time

## 모델

- Parking Success Rate
- Calibration
- False Positive
- False Negative

---

# 17. 개발 단계

## Phase 1 — MVP

- 공공데이터 adapter
- 주차장 DB
- 검색
- 가격 계산
- 추천
- Fact Check
- Android 기본 UX

## Phase 2 — 차별화

- 성공확률
- 신뢰도
- 현장 신고
- Plan B
- 입구 안내
- 출발 직전 재검증

## Phase 3 — 상용 서비스

- 로그인
- 사용자 계정
- 주차 타이머
- 알림
- 지도/경로
- 예약/주차권 제휴

## Phase 4 — 데이터 경쟁력

- 실제 성공 데이터
- 시간대별 예측
- 행사/날씨 변수
- ML 모델

## Phase 5 — 사업 확장

- 주차장 운영자 Dashboard
- B2B 분석
- 데이터 API
- 광고/제휴
- 프리미엄

---

# 18. 이번 V2 코드에 포함된 것

```text
backend/
  FastAPI
  Recommendation Engine
  Success Probability
  Confidence
  Feedback API
  Tests
  Dockerfile

worker/
  Data ingestion adapter 경계

android/
  Jetpack Compose UI
  추천 카드
  목적지/주차시간 입력

infra/
  PostgreSQL
  Redis

docs/
  상용화 계획
  API 계약
  보안
  아키텍처
```

---

# 19. 실제 출시 전에 반드시 추가할 것

현재 ZIP은 실제 운영계정 없이 실행 가능한 **Production Starter V2**다.

다음은 실제 상용계정/법무/운영환경이 필요하다.

- 실제 공공 API 연결
- 지도/경로 API
- 실제 인증
- PostgreSQL Repository 구현
- Redis cache
- 사용자 계정
- 위치정보 동의/처리
- 개인정보처리방침
- 약관
- 실제 결제/예약
- Push notification
- Crashlytics
- CI/CD
- Cloud deployment
- monitoring
- backup/restore
- penetration/security test
- Play Store release

---

# 20. 공식 기술 검증 메모

Android 공식 문서는 Compose에서 상태가 UI로 내려가고 이벤트가 위로 올라가는 UDF를 권장하며, ViewModel은 화면 수준에서 사용하고 하위 Composable에는 필요한 데이터/콜백만 전달하는 방식을 안내한다.

FastAPI 공식 문서는 Linux 컨테이너/Docker를 일반적인 배포 방식으로 설명하며, 컨테이너화가 보안·재현성·운영 단순화에 이점을 줄 수 있다고 설명한다.

따라서 V2 코드 구조는 이 방향을 따른다.

---

# 21. 최종 방향

```text
검색 앱
    ↓
추천 앱
    ↓
주차 성공 예측 앱
    ↓
주차 Journey Assistant
    ↓
주차 데이터 플랫폼
```

장기적으로는 단순 B2C 앱보다 **실제 주차 성공/실패 데이터**가 가장 중요한 자산이 된다.

---

# 22. 한 문장

> **“지금 어디에 세워야 할지 결정해주고, 실패하면 바로 다음 선택지를 주는 앱.”**

---

# 23. 1탄("오늘뭐하지") 실전 교훈 반영 체크리스트 (만복, 2026-08-29 추가)

> 착수는 1탄 Play Store 등록 완료 후로 유지. 다만 기획은 계속 다듬어야 한다는 바로보기님 판단에 따라, 안티에게 착수 지시 나가기 **전에** 1탄에서 실제로 겪은 사고를 미리 가드레일로 박아넣음. 전부 오늘 밤 실제로 벌어진 일들이지 가정이 아님.

## 23.1 시크릿/서명키 관리 — Phase 3(로그인/계정) 착수 전 필수
1탄에서 keystore 파일 git 커밋 → 재발급 → **비밀번호 문자열은 여전히 하드코딩되어 재노출** 순으로 2번 연속 사고가 났음(1차 조치가 절반만 됨을 3차 검증에서야 발견).
- **Go 조건**: `storePassword`/`keyPassword` 등 모든 시크릿은 처음부터 `local.properties`(gitignore 확인 필수) 또는 환경변수에서만 읽는다. 코드에 `?: "약한기본값"` 같은 **조용한 fallback을 절대 넣지 않는다** — 값이 없으면 빌드가 즉시 실패하게(`error("...")`) 만들 것.
- Backend(FastAPI)도 동일 원칙 — `.env.example`에 실제 값 예시를 안 넣더라도, 실제 `config.py`가 `os.getenv(..., "기본값")` 식으로 조용히 약한 기본값을 쓰지 않는지 초기 커밋부터 확인.

## 23.2 추천 엔진 — 점수 로직에 "우선순위 역전" 버그 패턴 주의
1탄 `hard_filter.py`에서 "N째주 휴무" 같은 특수 패턴이 "매주 휴무" 같은 일반 패턴에 먼저 걸려 오판정되는 순서 버그가 있었음(부분 문자열 매칭 조건 순서 문제).
- Section 4의 recommendation engine 구현 시, 여러 조건 분기(예: Plan A/B/C 선정, 성공확률 계산 규칙)가 **특수 케이스 → 일반 케이스 순서**로 검사되는지 코드 리뷰 단계에서 명시적으로 확인.
- Section 4 출력의 `plan_b`(Plan A/B/C)가 단순 점수 top-3만 뽑는 구조면, 1탄 score_engine.py처럼 "카테고리 다양성 부족"(같은 유형 주차장만 추천) 위험 있음 — top-k 이전에 유형별 최소 배분 로직을 처음부터 설계에 반영할 것.

## 23.3 완료보고 검증 — 처음부터 프레임워크 연결
1탄은 검증 스크립트(`verify_video.py`)를 나중에 만들었다가 "메타데이터만 보고 실제 디코딩은 안 봄"이라는 구멍이 있었음.
- 2탄은 `43_function_dev/03_verification_framework/verifiers.py`(video/json/pytest/dup 4종)를 **Phase 1 MVP 단계부터 재사용** — 예: backend 테스트는 `verifiers.py pytest`, 데이터 ingestion 결과 JSON은 `verifiers.py json`으로 완료보고에 실행 로그 첨부 의무화.
- "완료했습니다"만 있고 실행 로그가 없는 완료보고는 접수하지 않는다(AGENTS.md "완료보고 자동검증 우선 원칙" 그대로 적용).

## 23.4 Android 빌드 설정 — 처음부터 debug/release 분리
1탄은 `applicationIdSuffix` 없이 시작해서 debug/release APK가 같은 패키지명으로 충돌, 실기기 클린설치 실패 사고가 있었음.
- Section 10 Android 아키텍처 구현 시 `build.gradle.kts`의 `debug` 빌드타입에 처음부터 `applicationIdSuffix = ".debug"` 넣고 시작.

## 23.5 공공데이터 — API_REGISTRY.md 먼저 확인, 재신청 금지
1탄에서 "주차정보(B553881)" API는 **이미 2026-08-20에 활용신청 승인 완료**된 게 `65_android_apps/API_REGISTRY.md`에 기록돼있음(계정 공용키와 동일값). 2탄 착수 시 이 API를 다시 신청하거나 새 키를 받으려 하지 말고 그 표부터 확인.

## 23.6 문서-코드 정합성 — 수치는 항상 소스 대조
1탄 `FINAL_RELEASE_REPORT.md`에 minSdk/targetSdk 등 실제 코드와 다른 수치가 여러 번 남아있었음(코니가 매번 직접 소스 대조해서 잡아냄).
- 2탄 `docs/production-plan.md` 등 문서에 SDK 버전/의존성 버전 같은 구체적 수치를 적을 때마다, 그 문서를 업데이트하는 시점에 실제 `build.gradle.kts`/`requirements.txt`와 대조하는 걸 완료 기준에 포함.
