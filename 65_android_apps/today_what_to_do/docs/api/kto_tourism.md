# 한국관광공사 국문 관광정보 서비스 (KorService2)

## 출처
- 공공데이터포털: https://www.data.go.kr/data/15101578/openapi.do
- 참고문서: 한국관광공사41_국문 관광정보 서비스_오픈API활용가이드 (포털에서 다운로드)

## 인증
- Base URL: `https://apis.data.go.kr/B551011/KorService2`
- 인증키: 계정 단위 "일반인증키" (odcloud/기상청/반려동물과 동일값 공유 — 계정별 1개, API마다 개별 활용신청만 하면 됨)
- 저장 위치: `../../.env` → `KTO_SERVICE_KEY` (git 커밋 금지, gitignore 처리됨)

## 검증 완료 (2026-08-20)
`phase0/test_three_apis.py`의 `test_tour()`로 `areaCode2` 호출 → status 200, resultCode 0000, 지역코드 17건 정상 수신 확인.

## MVP에서 쓸 엔드포인트
- `areaCode2` — 지역코드 조회 (검증용으로 이미 확인됨)
- `locationBasedList2` — 현재 위치 기반 관광정보 조회 (핵심 — 사용자 GPS로 주변 장소 검색)
- `searchKeyword2` — 키워드 검색
- `searchFestival2` — 행사정보 조회
- `detailCommon2` — 공통 상세정보 (운영시간·주소·전화 등)
- `detailIntro2` — 소개정보 (휴무일 등)
- `detailImage2` — 이미지정보
- `detailPetTour2` — 반려동물 동반 정보

## 공통 필수 파라미터
| 파라미터 | 값 | 비고 |
|---|---|---|
| `serviceKey` | `.env`의 `KTO_SERVICE_KEY` | |
| `numOfRows` | 요청 건수 | |
| `pageNo` | 페이지 번호 | |
| `MobileOS` | `ETC` | Android면 `AND` |
| `MobileApp` | 앱 이름 (임의 문자열) | |
| `_type` | `json` | 안 넣으면 XML 응답 |

## 이미지 저작권 주의
관광정보 API의 사진은 데이터 본문과 별개 이용조건이 붙을 수 있음 — 상용 앱에서는 이미지마다 이용 가능 범위를 개별 확인 후 사용 (제품 기획서 6.1절 참조).

## 다음 확인할 것
- `locationBasedList2`에 실제 GPS 좌표 넣어서 응답 필드 구조 확인 (거리순 정렬 여부, 반환 필드 목록)
- `detailIntro2`로 실제 휴무일 필드명 확인 (Hard Filter에 쓸 예정)
