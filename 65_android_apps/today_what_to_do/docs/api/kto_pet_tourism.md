# 한국관광공사 반려동물 동반여행 서비스 (KorPetTourService2)

## 출처
- 공공데이터포털: https://www.data.go.kr/data/15135102/openapi.do
- 참고문서: 개방데이터_활용매뉴얼(반려동물동반여행).zip (포털에서 다운로드)

## 인증
- Base URL: `https://apis.data.go.kr/B551011/KorPetTourService2`
- 인증키: KorService2(관광정보)와 동일한 계정 단위 일반인증키
- 저장 위치: `../../.env` → `KTO_PET_SERVICE_KEY` (git 커밋 금지)

## 검증 완료 (2026-08-20)
`phase0/test_three_apis.py`의 `test_pet()`로 `areaCode2` 호출 → status 200, resultCode 0000, 지역코드 17건 정상 수신 확인. API 구조는 KorService2와 동일한 패턴(엔드포인트명, 파라미터명 공유).

## MVP에서 쓸 엔드포인트
- `areaCode2` — 지역코드 조회 (검증용으로 이미 확인됨)
- `locationBasedList2` — 현재 위치 기반 반려동물 동반 가능 장소 조회
- `areaBasedList2` — 지역기반 조회
- `detailPetTour2` — **반려동물 동반 조건 상세** (핵심 — Hard Filter의 `pet_allowed` 판정에 사용)
- `detailCommon2` / `detailIntro2` — 공통/소개 정보
- `detailImage2` — 이미지

## 공통 필수 파라미터
KorService2와 동일: `serviceKey`, `numOfRows`, `pageNo`, `MobileOS`, `MobileApp`, `_type=json`

## 앱 연결 흐름
```
사용자 "강아지와 갈 곳" 선택
    ↓
반려동물 조건 ON
    ↓
locationBasedList2 (또는 areaBasedList2)
    ↓
detailPetTour2로 동반 가능 조건 상세 확인
    ↓
날씨 + 거리 + 영업시간 결합 → 추천
```

## 다음 확인할 것
- `detailPetTour2` 실제 응답에서 "동반 가능/불가" 판정 필드명 확인
- KorService2와 데이터 중복 여부(같은 장소가 양쪽에 다 있는지, place_id 매칭 가능한지) — 앱 DB의 `place` 테이블에 두 소스를 어떻게 병합할지 결정 필요
