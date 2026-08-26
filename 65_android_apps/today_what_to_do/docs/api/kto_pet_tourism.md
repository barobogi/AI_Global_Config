# 한국관광공사 반려동물 동반여행 서비스 (KorPetTourService2)

## 출처
- 공공데이터포털: https://www.data.go.kr/data/15135102/openapi.do
- 참고문서: 개방데이터_활용매뉴얼(반려동물동반여행).zip (포털에서 다운로드)

## 인증
- Base URL: `https://apis.data.go.kr/B551011/KorPetTourService2`
- 인증키: KorService2(관광정보)와 동일한 계정 단위 일반인증키
- 저장 위치: `../../.env` → `KTO_PET_SERVICE_KEY` (git 커밋 금지)

## 검증 완료 (2026-08-20)
1. `phase0/test_three_apis.py`의 `test_pet()`로 `areaCode2` 호출 → status 200, resultCode 0000, 지역코드 17건 정상 수신 확인.
2. `locationBasedList2` 및 `detailPetTour2` 실호출 및 응답 필드 분석 완료.

## MVP 핵심 엔드포인트 및 응답 필드 구조

### 1. `locationBasedList2` (반려동물 동반 가능 장소 위치 검색)
- KorService2와 동일한 요청 규격 (`mapX`, `mapY`, `radius`, `arrange=E`)
- 반환되는 모든 장소는 기본적으로 반려동물 동반 관련 시설/여행지임.

### 2. `detailPetTour2` (반려동물 동반 조건 상세)
- **주요 응답 필드**:
  - `acmpyTypeCd`: 동반 유형 코드 (동반 가능 / 조건부 동반 등)
  - `acmpyNeedMtr`: 동반 시 필수 준비물 (목줄, 배변봉투, 케이지 등)
  - `relaAcdntRiskMtr`: 사고 대비 주의사항
  - `relaPosesFclty`: 구비 시설 (놀이터, 배변판 등)
  - `relaFrnshPrdlst`: 비치 품목
  - `etcAcmpyInfo`: 기타 동반 제한/안내 사항

## 9.1절 Hard Filter 연동 가이드
- **`user_with_pet = True` 시**:
  1. `KorPetTourService2` 출처 데이터(`is_pet_spot=True`) 우선 통과
  2. 일반 `KorService2` 데이터의 경우 제목/개요에 '반려견', '애견', '반려동물' 키워드가 포함된 장소만 통과
  3. 그 외 장소는 `pet` 필터 단계에서 탈락 (`reject_reason: 반려동물 동반 불가/정보 없음`)

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
