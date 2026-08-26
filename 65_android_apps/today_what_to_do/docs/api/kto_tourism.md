# 한국관광공사 국문 관광정보 서비스 (KorService2)

## 출처
- 공공데이터포털: https://www.data.go.kr/data/15101578/openapi.do
- 참고문서: 한국관광공사41_국문 관광정보 서비스_오픈API활용가이드 (포털에서 다운로드)

## 인증
- Base URL: `https://apis.data.go.kr/B551011/KorService2`
- 인증키: 계정 단위 "일반인증키" (odcloud/기상청/반려동물과 동일값 공유 — 계정별 1개, API마다 개별 활용신청만 하면 됨)
- 저장 위치: `../../.env` → `KTO_SERVICE_KEY` (git 커밋 금지, gitignore 처리됨)

## 검증 완료 (2026-08-20)
1. `phase0/test_three_apis.py`의 `test_tour()`로 `areaCode2` 호출 → status 200, resultCode 0000, 지역코드 17건 정상 수신 확인.
2. `backend/data_collector.py`로 서울 주요 거점(시청/강남/홍대/잠실/종로) `locationBasedList2` 및 `detailIntro2` 실호출 및 응답 구조 분석 완료.

## MVP 핵심 엔드포인트 및 응답 필드 구조

### 1. `locationBasedList2` (위치 기반 장소 조회)
- **요청 파라미터**: `mapX`(경도), `mapY`(위도), `radius`(반경m, 최대 20000), `arrange=E`(거리순 정렬)
- **주요 응답 필드**:
  - `contentid`: 콘텐츠 고유 ID
  - `contenttypeid`: 12(관광지), 14(문화시설), 15(축제), 28(레포츠), 38(쇼핑), 39(음식점)
  - `title`: 장소명
  - `addr1`: 기본 주소
  - `mapx`, `mapy`: WGS84 좌표 (경도, 위도)
  - `dist`: 중심점 기준 거리 (미터)
  - `firstimage`: 대표 썸네일 이미지 URL
  - `tel`: 전화번호

### 2. `detailIntro2` (운영시간·휴무일·이용요금 상세소개)
- **contentTypeId별 핵심 필드 매핑**:
  | contentTypeId | 분류 | 이용시간 필드 | 휴무일 필드 | 이용요금 필드 | 체험연령 |
  |---|---|---|---|---|---|
  | **12** | 관광지 | `usetime` | `restdate` | `usefee` | `expagerange` |
  | **14** | 문화시설 | `usetimeculture` | `restdateculture` | `usefeeculture` | `spendtime` |
  | **15** | 축제/행사 | `usetimefestival` | `eventenddate` | `usefee` | `spendtimefestival` |
  | **28** | 레포츠 | `usetimeleports` | `restdateleports` | `usefeeleports` | `expagerangeleports` |
  | **38** | 쇼핑 | `opentime` | `restdateshopping` | - | - |
  | **39** | 음식점 | `opentimefood` | `restdatefood` | - | `treatmenu` |

## 9.1절 Hard Filter 연동 가이드
- **영업 여부 (`is_open`)**: `restdate*` 필드에서 요일별 정기휴무 문자열(`매주 월요일`, `화요일 휴무` 등) 파싱 대조
- **예산 검증 (`budget`)**: `usefee*` 필드에서 숫자(원 단위) 정규식 추출 후 `price > budget` 검사
- **거리 계산 (`distance`)**: `mapx`, `mapy` 하버사인(Haversine) 거리 계산 (사용자 반경 필터링)
- **실내/실외 구분**: `contenttypeid` 14/38/39 및 키워드(박물관/미술관/몰/실내) 기반 분류 ➔ 강수확률 60% 이상 시 실외 필터링/감점
