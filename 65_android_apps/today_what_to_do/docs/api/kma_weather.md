# 기상청 단기예보 조회서비스 (VilageFcstInfoService_2.0)

## 출처
- 공공데이터포털: https://www.data.go.kr/data/15084084/openapi.do
- 참고문서: 기상청41_단기예보 조회서비스_오픈API활용가이드_2607.zip (포털에서 다운로드)

## 인증
- Base URL: `https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0`
- 인증키: 관광정보/반려동물과 동일한 계정 단위 일반인증키
- 저장 위치: `../../.env` → `KMA_SERVICE_KEY` (git 커밋 금지)

## 검증 완료 (2026-08-20)
`phase0/test_three_apis.py`의 `test_weather()`로 `getVilageFcst` 호출(서울시청 격자 nx=60, ny=127) → status 200, resultCode **00** NORMAL_SERVICE, 실제 예보 데이터 정상 수신.

실제 응답 예시(2026-08-20 08:00 발표분, 09:00 예보):
```json
{"baseDate":"20260820","baseTime":"0800","category":"TMP","fcstDate":"20260820","fcstTime":"0900","fcstValue":"26","nx":60,"ny":127}
```
TMP(기온)=26, 그 외 UUU/VVV(풍속성분)/VEC(풍향)/WSD(풍속) 등 카테고리별로 행이 나뉘어 반환됨.

## 핵심 함정 — 발표시각(base_time)
02, 05, 08, 11, 14, 17, 20, 23시에만 발표되고, **발표 후 10분 뒤부터** 조회 가능. 이 시각이 아니거나 너무 이르게 요청하면 빈 응답/에러. `phase0/test_three_apis.py`의 `latest_base_time()` 함수가 현재시각 기준 가장 최근 유효 발표시각을 자동 계산함 — 재사용할 것.

## 핵심 함정 — 좌표계
위경도(lat/lng)를 직접 안 받고 기상청 자체 격자좌표 `nx`, `ny`를 씀. Android GPS 좌표 → 격자좌표 변환 함수를 Backend에 별도로 둬야 함(공식 변환식은 기상청 참고문서의 격자변환 공식 참조 — 위 zip 안에 포함).

| 지역 예시 | nx | ny |
|---|---|---|
| 서울시청 | 60 | 127 |

## MVP에서 쓸 엔드포인트
- `getVilageFcst` — 단기예보(최대 3일치, category별 다수 행) — **검증 완료, 이거 하나로 MVP 충분**
- `getUltraSrtNcst` — 초단기실황(현재 관측값)
- `getUltraSrtFcst` — 초단기예보(6시간 이내)

## 응답 category 코드 (자주 쓸 것만)
| 코드 | 의미 |
|---|---|
| TMP | 기온(℃) |
| POP | 강수확률(%) |
| PTY | 강수형태 |
| SKY | 하늘상태 |
| WSD | 풍속 |

## 다음 확인할 것
- `POP`(강수확률) 필드로 실외 장소 감점 로직(9.1절 Hard Filter의 `rain_probability > 60`) 실제 구현
- GPS → nx,ny 격자변환 함수 Backend에 구현
