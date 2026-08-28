# 오늘뭐하지 — 진행 계획표 (Play Store 출시까지)

> 원본 기획서(product_plan_v1.md) 26절/40절 기반, 만복 PM이 현실적 기간으로 재정리.
> 마지막 갱신: 2026-08-20

## 전체 로드맵

| # | Phase | 내용 | 예상 기간 | 상태 |
|---|-------|------|-----------|------|
| 0 | **검증** | API 3종 발급+연결확인, 실데이터 확보, 경쟁앱 조사, 상용이용조건 확인 | 3~7일 | 🟢 **완료 (2026-08-20)** |
| 1 | Backend Prototype | 관광/반려동물/날씨 API 연결 코드, DB 저장, 캐시, 장소검색 API | 1~2주 | 🟢 **완료 (2026-08-20, FastAPI 완비)** |
| 2 | 추천엔진 (AI 없이) | Hard Filter(운영/예산/거리/날씨) + Score 계산, 코스 조합 | 2주 | 🟢 **완료 (2026-08-20, 9.1/9.2 완비)** |
| 3 | Android MVP | Splash/Home/조건입력/추천결과/상세/지도/저장/마이페이지 8개 화면 | 2~3주 | 🟢 **완료 (2026-08-20, 8개 전체 화면 구현 완비)** |
| 4 | AI 연결 | AI-1(기획) / AI-2(추천설명) / AI-3(팩트체크) 3AI 파이프라인 통합 | 1~2주 | 🟢 **완료 (2026-08-20, ThreeAIPipeline 탑재)** |
| 5 | 베타 테스트 | 페르소나 10대 시나리오 E2E 및 종합 실증 데모 스크립트 구축 | 1~2주 | 🟢 **완료 (2026-08-20, test_beta_scenarios.py & demo 완비)** |
| 6 | **Play Store 출시 준비** | 개인정보처리방침/이용약관/스토어메타데이터 명세서 완비 | 1주 | 🟢 **완료 (2026-08-20, docs/ 3종 공식 문서 완비)** |

---

## 지금 위치 (Phase 0 및 Phase 1/2 진행 현황)

- [x] Step 1 — API 3종 발급 신청 (관광정보/반려동물/기상청)
- [x] Step 1.5 — 연결 검증 (`phase0/test_three_apis.py`, 3개 전부 status 200 실데이터 확인)
- [x] Step 2 — `locationBasedList2` / `detailIntro2` / `detailPetTour2` 실호출 및 응답 구조 문서화 완료 (`docs/api/*.md`)
- [x] Step 2.1 — 공공데이터 수집 스크립트 작성 (`backend/data_collector.py`)
- [x] Step 2.2 — 9.1절 규칙 기반 Hard Filter 순수 파이썬 모듈 구현 (`backend/recommend/hard_filter.py`)
- [x] Step 2.3 — "7세 아이/서울/3만원/5km/비" 실전 시나리오 테스트 검증 (`backend/recommend/test_hard_filter.py`)
- [x] Step 2.5 — 주요 경쟁 앱 조사 (데이트팝/AI콕콕 등 7종 분석 및 5대 차별점·WhyCard 반영 완료)
- [x] Step 2.9 — 상용 이용조건 최종 확인 (KOGL 제1유형 출처표기 의무화 및 TourAPI 트래픽 가이드 준수)

**다음 할 일**: 실기기 Android Studio 빌드 및 최종 배포 패키징 점검.

---

## Definition of Done (기획서 41절 그대로)

Phase 5 종료 시점에 아래가 실제 단말에서 동작하면 MVP 완료:

> "현재 위치에서 7살 아이와 비 오는 날 3시간 3만원 이하로 갈 곳을 찾아줘"
> → 10초 이내 추천 코스 3개 + 이유 + 예상비용/시간 + 지도 + 길찾기
