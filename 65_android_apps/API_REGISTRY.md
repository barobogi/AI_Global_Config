# 65번 뿌리 — 공공데이터 API 활용신청 현황

> 새 앱 시작 전 여기부터 확인 — 이미 신청된 API면 재신청 불필요(같은 계정키로 바로 사용 가능).
> 키 저장 위치: `65_android_apps/.env` (신규 앱 공통) — 상세는 `PUBLIC_DATA_STRATEGY.md` 참조.

| API | 제공기관코드 | 활용신청 상태 | 사용 중인 앱 | 문서 |
|---|---|---|---|---|
| 국문 관광정보 서비스 (KorService2) | B551011 | ✅ 승인 | today_what_to_do (1탄) | `today_what_to_do/docs/api/kto_tourism.md` |
| 반려동물 동반여행 (KorPetTourService2) | B551011 | ✅ 승인 | today_what_to_do (1탄) | `today_what_to_do/docs/api/kto_pet_tourism.md` |
| 기상청 단기예보 (VilageFcstInfoService_2.0) | 1360000 | ✅ 승인 | today_what_to_do (1탄) | `today_what_to_do/docs/api/kma_weather.md` |
| 공공데이터포털 목록조회 (odcloud) | 15077093 | ✅ 승인 | (연결검증용) | `today_what_to_do/phase0/test_odcloud_key.py` |
| 한국교통안전공단 주차정보 (Parking) | B553881 | ✅ 승인 (2026-08-20 밤 확인, 기존 계정키와 동일값) | parking_where (2탄 예정, 착수는 1탄 완료 후) | End Point: `https://apis.data.go.kr/B553881/Parking`, 데이터포맷 JSON+XML, 참고문서 `65_android_apps/Idea/주차정보시스템_기술문서_수정본_20240702.docx` |

## 활용신청 절차 (참고용 — 현재 대상 API 전부 승인 완료)
1. data.go.kr 해당 API 상세 페이지 접속 → 로그인
2. [오픈API 상세] → [활용신청] → 활용목적 간단 입력
3. 승인 후 마이페이지에서 인증키 확인 (지금까지 5개 전부 동일 계정키로 확인됨)
4. 이 표의 상태를 ✅로 갱신
