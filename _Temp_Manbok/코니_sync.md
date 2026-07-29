# 코니 세션 싱크 파일
**자동 생성**: 2026-07-29 19:03 (master_watch.py)
**읽는 법**: 이 파일 내용을 코니에게 붙여넣으면 만복이와 즉시 동기화됨.

---

## 현재 프로젝트 상태

# 📋 Next Projects — Barobogi + 만복

**최초 작성**: 2026-06-21  
**최종 업데이트**: 2026-07-19  
**상태**: 뽀개기 자동화 v2 구현 중 / Hermes 도출 Task 3건 신규 등록

### 📌 신규 등록 (2026-07-19 — Hermes Agent 뽀개기 도출)

> ⚠️ 뿌리체계 진행 상황에 따라 일정 당겨질 수 있음

| Task | 내용 | 뿌리 | 예정 | 담당 |
|------|------|------|------|------|
| **T-TG-TOPIC** | Telegram 멀티 Topic 연동 — 코니/안티/만복 채널 분리 + 모바일 원격 제어 | 24번 (협업도구) | 2026-07-26 전후 | 안티 |
| **T-GOAL-LOOP** | /goal 자가치유 루프 통합 — 뽀개기 7~8단계 자동 재시도 엔진 | 28번 (에이전트) | 2026-08-02 전후 | 안티+만복 |
| **T-VPS-DEPLOY** | here.now VPS 자동 배포 파이프라인 — 로컬 → VPS 전환 24/7 운영 | 23번 (배포인프라) | 2026-08 중순 | 안티 |

> /goal 제어 기준 확정: 최대 20턴 + 1시간 + 할당량 75% 중 하나 충족 시 자동 중단

### 📋 다음 작업 스케쥴 (2026-07-13 확정 — 상세 논의 내일)

| 순위 | Task | 비고 |
|------|------|------|
| 1 | **T026** MSA/하이브리드 로깅 | 파일럿 범위 만복↔안티 한정, 코니 비상주 제약 안티에 확인 필수, n8n Webhook 재사용 |
| 2 | **T025** Docker Phase1 | T026과 병행 가능, Volume/속도/네트워크 체크 후 착수 |
| 3 | **T063** YouTube 자율운영 ③→④ | ③시각가이드라인→④댓글분류 순서, ⑤는 ③④ 안정 후 |
| 후 | **T024** VibeCoding 웹앱 제너레이터 | 뿌리64 신설·보안설계·T020재사용 선행 조건 3개 해소 후 |

### ✅ 2026-07-11 완료 (저녁)

- **T011/T018/T019 completed** — master_watch.py push 즉시 브리핑 갱신, youtube_pobbagi.py --video-id 추가

---

## 오늘 커밋 요약

**stock_dashboard**
- a9a966a auto: Cowork/CLI 동기화 2026-07-29 19:00
- 19a5f61 auto: 현재가 갱신 2026-07-29T18:00 현재가:35개
- 1800a38 auto: 현재가 갱신 2026-07-29T16:00 현재가:35개
- 7ebfe14 auto: 현재가 갱신 2026-07-29T15:00 현재가:35개
- 3651a92 auto: 현재가 갱신 2026-07-29T14:00 현재가:35개
- 144b980 auto: 현재가 갱신 2026-07-29T13:00 현재가:35개
- b83b3cb auto: 현재가 갱신 2026-07-29T12:00 현재가:35개
- 752b33c auto: 현재가 갱신 2026-07-29T11:00 현재가:35개
- d72ae28 auto: 현재가 갱신 2026-07-29T10:00 현재가:35개
- b6258fc auto: 현재가 갱신 2026-07-29T09:00 현재가:35개
- 65f2b21 auto: 현재가 갱신 2026-07-29T08:00 현재가:35개
- 8d8c91f auto: 현재가 갱신 2026-07-29T06:00 현재가:35개
- 9330d06 auto: 현재가 갱신 2026-07-29T04:00 현재가:35개
- 06a5880 auto: 현재가 갱신 2026-07-29T02:00 현재가:35개
- 309e8ab auto: 현재가 갱신 2026-07-29T00:00 현재가:35개

**Daily_for_Barobogi**
- 63e9813 auto: Cowork/CLI 동기화 2026-07-29 18:09
- ffc353b auto: Cowork/CLI 동기화 2026-07-29 18:00
- 6512de8 auto: Cowork/CLI 동기화 2026-07-29 16:09
- 19d343a auto: Cowork/CLI 동기화 2026-07-29 16:00
- 3d25be5 auto: Cowork/CLI 동기화 2026-07-29 15:00
- d21624b auto: Cowork/CLI 동기화 2026-07-29 14:00
- 07a2314 auto: Cowork/CLI 동기화 2026-07-29 13:00
- 0de16ab auto: Cowork/CLI 동기화 2026-07-29 12:00
- b69023a auto: Cowork/CLI 동기화 2026-07-29 11:00
- e77493b auto: Cowork/CLI 동기화 2026-07-29 10:00
- 1123ee6 auto: Cowork/CLI 동기화 2026-07-29 09:00
- 7e0075b auto: Cowork/CLI 동기화 2026-07-29 08:00
- 6699d13 auto: Cowork/CLI 동기화 2026-07-29 06:00
- 88689b2 auto: Cowork/CLI 동기화 2026-07-29 05:08
- b8db3d7 auto: Cowork/CLI 동기화 2026-07-29 04:07
- 6aafea4 auto: Cowork/CLI 동기화 2026-07-29 04:00
- b086662 auto: Cowork/CLI 동기화 2026-07-29 02:00
- 6f05e95 auto: Cowork/CLI 동기화 2026-07-29 01:07
- b58dde3 auto: Cowork/CLI 동기화 2026-07-29 01:07
- c4587b2 auto: Cowork/CLI 동기화 2026-07-29 00:06
- 2bea6f1 auto: Cowork/CLI 동기화 2026-07-29 00:00

**260623_1_study_all**
- e2ab9fc auto: Cowork/CLI 동기화 2026-07-29 08:00

**AI_Global_Config**
- 53fd538d3 auto: Cowork/CLI 동기화 2026-07-29 19:03
- 7591b548d auto: Cowork/CLI 동기화 2026-07-29 19:03
- b335f1c0f auto: Cowork/CLI 동기화 2026-07-29 19:02
- 2bb701e93 auto: Cowork/CLI 동기화 2026-07-29 19:02
- fe263d66e auto: Cowork/CLI 동기화 2026-07-29 19:00
- b18c671b6 auto: Cowork/CLI 동기화 2026-07-29 18:57
- 0fcc5d853 auto: Cowork/CLI 동기화 2026-07-29 18:57
- 72a091651 auto: Cowork/CLI 동기화 2026-07-29 18:52
- b71daa444 auto: Cowork/CLI 동기화 2026-07-29 18:52
- 28eab57e8 auto: Cowork/CLI 동기화 2026-07-29 18:47
- fdbf27d79 auto: Cowork/CLI 동기화 2026-07-29 18:47
- fabfa650c auto: Cowork/CLI 동기화 2026-07-29 18:42
- 39b277e7a auto: Cowork/CLI 동기화 2026-07-29 18:42
- c54356abe auto: Cowork/CLI 동기화 2026-07-29 18:37
- 0e1678db6 auto: Cowork/CLI 동기화 2026-07-29 18:37
- 54b0e8f61 auto: Cowork/CLI 동기화 2026-07-29 18:32
- fa55ee413 auto: Cowork/CLI 동기화 2026-07-29 18:32
- bd21f6456 auto: Cowork/CLI 동기화 2026-07-29 18:27
- dfb0ea615 auto: Cowork/CLI 동기화 2026-07-29 18:27
- 14b240f80 auto: Cowork/CLI 동기화 2026-07-29 18:22
- 2e4c0709a auto: Cowork/CLI 동기화 2026-07-29 18:22
- 2986720f1 auto: Cowork/CLI 동기화 2026-07-29 18:17
- 68bb161fa auto: Cowork/CLI 동기화 2026-07-29 18:17
- 184c871da auto: Cowork/CLI 동기화 2026-07-29 18:12
- 63598b43d auto: Cowork/CLI 동기화 2026-07-29 18:12
- 135b889d7 auto: Cowork/CLI 동기화 2026-07-29 18:08
- bc6891e48 auto: Cowork/CLI 동기화 2026-07-29 18:08
- 9a8736686 auto: Cowork/CLI 동기화 2026-07-29 18:07
- c32585406 auto: Cowork/CLI 동기화 2026-07-29 18:07
- 41236a7ef auto: Cowork/CLI 동기화 2026-07-29 18:02
- 7a025b1ac auto: Cowork/CLI 동기화 2026-07-29 18:02
- 7309a64a9 auto: Cowork/CLI 동기화 2026-07-29 18:01
- 6c4cf4fcd auto: Cowork/CLI 동기화 2026-07-29 18:01
- 77f879e92 auto: Cowork/CLI 동기화 2026-07-29 17:57
- 8b00234ec auto: Cowork/CLI 동기화 2026-07-29 17:57
- 4e29cd287 auto: Cowork/CLI 동기화 2026-07-29 17:52
- 5a93e6ea5 auto: Cowork/CLI 동기화 2026-07-29 17:52
- da9b54c9b auto: Cowork/CLI 동기화 2026-07-29 17:47
- ceaeaa48b auto: Cowork/CLI 동기화 2026-07-29 17:47
- 48c865698 auto: Cowork/CLI 동기화 2026-07-29 17:42
- d0341df59 auto: Cowork/CLI 동기화 2026-07-29 17:42
- 10f9a7f44 auto: Cowork/CLI 동기화 2026-07-29 17:37
- 5cf2d8cda auto: Cowork/CLI 동기화 2026-07-29 17:37
- 1af5670df auto: Cowork/CLI 동기화 2026-07-29 17:32
- 11b753636 auto: Cowork/CLI 동기화 2026-07-29 17:32
- bb3c5af5f auto: Cowork/CLI 동기화 2026-07-29 17:27
- 46db8c9a5 auto: Cowork/CLI 동기화 2026-07-29 17:27
- bdf8bf41e auto: Cowork/CLI 동기화 2026-07-29 17:22
- 78cdbce5f auto: Cowork/CLI 동기화 2026-07-29 17:22
- ed589f8e5 auto: Cowork/CLI 동기화 2026-07-29 17:22
- 56151037b auto: Cowork/CLI 동기화 2026-07-29 17:17
- e051b020d auto: Cowork/CLI 동기화 2026-07-29 17:17
- 09afffab9 auto: Cowork/CLI 동기화 2026-07-29 17:17
- fabbae3f2 auto: Cowork/CLI 동기화 2026-07-29 17:12
- 3ff974467 auto: Cowork/CLI 동기화 2026-07-29 17:12
- a89707f4e auto: Cowork/CLI 동기화 2026-07-29 17:12
- d393235f9 auto: Cowork/CLI 동기화 2026-07-29 17:07
- 81eb298b4 auto: Cowork/CLI 동기화 2026-07-29 17:07
- 2c106c0dc auto: Cowork/CLI 동기화 2026-07-29 17:07
- 902af4b39 auto: Cowork/CLI 동기화 2026-07-29 17:02
- 229e7364d auto: Cowork/CLI 동기화 2026-07-29 17:02
- cadda6691 auto: Cowork/CLI 동기화 2026-07-29 17:02
- 57250a57e auto: Cowork/CLI 동기화 2026-07-29 16:57
- b904f2d4f auto: Cowork/CLI 동기화 2026-07-29 16:57
- 8655dcbd1 auto: Cowork/CLI 동기화 2026-07-29 16:57
- 7148a418d auto: Cowork/CLI 동기화 2026-07-29 16:52
- 524798a32 auto: Cowork/CLI 동기화 2026-07-29 16:52
- c7a401ac2 auto: Cowork/CLI 동기화 2026-07-29 16:52
- 7328b2801 auto: Cowork/CLI 동기화 2026-07-29 16:47
- 47588a03d auto: Cowork/CLI 동기화 2026-07-29 16:47
- 4a8178634 auto: Cowork/CLI 동기화 2026-07-29 16:47
- 1419a8a79 auto: Cowork/CLI 동기화 2026-07-29 16:42
- e2b07e9c2 auto: Cowork/CLI 동기화 2026-07-29 16:42
- 16b483ae8 auto: Cowork/CLI 동기화 2026-07-29 16:42
- 4b3db2251 auto: Cowork/CLI 동기화 2026-07-29 16:37
- 2b6be4d5d auto: Cowork/CLI 동기화 2026-07-29 16:37
- be3e0ca36 auto: Cowork/CLI 동기화 2026-07-29 16:37
- 48f77934b auto: Cowork/CLI 동기화 2026-07-29 16:32
- eb4c622d9 auto: Cowork/CLI 동기화 2026-07-29 16:32
- ba229b26c auto: Cowork/CLI 동기화 2026-07-29 16:32
- 31cd39933 auto: Cowork/CLI 동기화 2026-07-29 16:27
- 4acdcec39 auto: Cowork/CLI 동기화 2026-07-29 16:27
- e3df97798 auto: Cowork/CLI 동기화 2026-07-29 16:27
- a4c80ead2 auto: Cowork/CLI 동기화 2026-07-29 16:22
- fce78cce5 auto: Cowork/CLI 동기화 2026-07-29 16:22
- 21dafbafc auto: Cowork/CLI 동기화 2026-07-29 16:22
- f9af5f9e3 auto: Cowork/CLI 동기화 2026-07-29 16:17
- feda80477 auto: Cowork/CLI 동기화 2026-07-29 16:17
- 20750a776 auto: Cowork/CLI 동기화 2026-07-29 16:17
- 1b4cb73e3 auto: Cowork/CLI 동기화 2026-07-29 16:12
- e555b2813 auto: Cowork/CLI 동기화 2026-07-29 16:12
- 8513daf7e auto: Cowork/CLI 동기화 2026-07-29 16:12
- dd450921e auto: Cowork/CLI 동기화 2026-07-29 16:08
- 8b4ebe8eb auto: Cowork/CLI 동기화 2026-07-29 16:08
- 9e81ff749 auto: Cowork/CLI 동기화 2026-07-29 16:07
- 8b33c56cc auto: Cowork/CLI 동기화 2026-07-29 16:07
- f397c2ab0 auto: Cowork/CLI 동기화 2026-07-29 16:07
- 16bb1fc8a auto: Cowork/CLI 동기화 2026-07-29 16:02
- 1d289e6f5 auto: Cowork/CLI 동기화 2026-07-29 16:02
- 7ce0e6460 auto: Cowork/CLI 동기화 2026-07-29 16:02
- 85d9f09aa auto: Cowork/CLI 동기화 2026-07-29 15:57
- 805d90efe auto: Cowork/CLI 동기화 2026-07-29 15:57
- 0a6217ac1 auto: Cowork/CLI 동기화 2026-07-29 15:57
- b4bcc43fd auto: Cowork/CLI 동기화 2026-07-29 15:52
- ce1f1f651 auto: Cowork/CLI 동기화 2026-07-29 15:52
- e7b75b017 auto: Cowork/CLI 동기화 2026-07-29 15:52
- a6d2754dc auto: Cowork/CLI 동기화 2026-07-29 15:47
- 540ffeb08 auto: Cowork/CLI 동기화 2026-07-29 15:47
- 892a49abf auto: Cowork/CLI 동기화 2026-07-29 15:47
- 47d16176e auto: Cowork/CLI 동기화 2026-07-29 15:42
- 465810a89 auto: Cowork/CLI 동기화 2026-07-29 15:42
- 78278f3e2 auto: Cowork/CLI 동기화 2026-07-29 15:42
- f46b62878 auto: Cowork/CLI 동기화 2026-07-29 15:37
- a13c03d32 auto: Cowork/CLI 동기화 2026-07-29 15:37
- 3323d9a7d auto: Cowork/CLI 동기화 2026-07-29 15:37
- da7b66186 auto: Cowork/CLI 동기화 2026-07-29 15:32
- c93e2f613 auto: Cowork/CLI 동기화 2026-07-29 15:32
- 6d72192b6 auto: Cowork/CLI 동기화 2026-07-29 15:32
- 71f7614fb auto: Cowork/CLI 동기화 2026-07-29 15:27
- c4f9aec96 auto: Cowork/CLI 동기화 2026-07-29 15:27
- fa27ed4ec auto: Cowork/CLI 동기화 2026-07-29 15:27
- 28c73292c auto: Cowork/CLI 동기화 2026-07-29 15:22
- 5457b4a39 auto: Cowork/CLI 동기화 2026-07-29 15:22
- 4bf9a94e5 auto: Cowork/CLI 동기화 2026-07-29 15:22
- 8bb0312eb auto: Cowork/CLI 동기화 2026-07-29 15:17
- 1c1a3e2e5 auto: Cowork/CLI 동기화 2026-07-29 15:17
- 7b55d85af auto: Cowork/CLI 동기화 2026-07-29 15:17
- 606d47782 auto: Cowork/CLI 동기화 2026-07-29 15:12
- 21d058f08 auto: Cowork/CLI 동기화 2026-07-29 15:12
- 025d1aa93 auto: Cowork/CLI 동기화 2026-07-29 15:12
- 020c69692 auto: Cowork/CLI 동기화 2026-07-29 15:07
- b8c0a9772 auto: Cowork/CLI 동기화 2026-07-29 15:07
- aa9b9d22b auto: Cowork/CLI 동기화 2026-07-29 15:07
- b835001ce auto: Cowork/CLI 동기화 2026-07-29 15:02
- 2c82b94c9 auto: Cowork/CLI 동기화 2026-07-29 15:02
- c0d0bde3b auto: Cowork/CLI 동기화 2026-07-29 15:02
- 8cfd59731 auto: Cowork/CLI 동기화 2026-07-29 14:57
- c7b30e94a auto: Cowork/CLI 동기화 2026-07-29 14:57
- 4bfe6954b auto: Cowork/CLI 동기화 2026-07-29 14:57
- 44cea28fe auto: Cowork/CLI 동기화 2026-07-29 14:52
- 79ef11e89 auto: Cowork/CLI 동기화 2026-07-29 14:52
- 8170e875a auto: Cowork/CLI 동기화 2026-07-29 14:52
- 1dcafad8c auto: Cowork/CLI 동기화 2026-07-29 14:47
- 99f61d4b9 auto: Cowork/CLI 동기화 2026-07-29 14:47
- 78bf8b109 auto: Cowork/CLI 동기화 2026-07-29 14:47
- 9c242161c auto: Cowork/CLI 동기화 2026-07-29 14:42
- 7f8561c99 auto: Cowork/CLI 동기화 2026-07-29 14:42
- bee2b9967 auto: Cowork/CLI 동기화 2026-07-29 14:42
- 66aa4e19d auto: Cowork/CLI 동기화 2026-07-29 14:37
- 7bfd36d6b auto: Cowork/CLI 동기화 2026-07-29 14:37
- 309df6709 auto: Cowork/CLI 동기화 2026-07-29 14:37
- 22c7e3e51 auto: Cowork/CLI 동기화 2026-07-29 14:32
- 51b422bb1 auto: Cowork/CLI 동기화 2026-07-29 14:32
- 8f0a93dee auto: Cowork/CLI 동기화 2026-07-29 14:32
- f4093848d auto: Cowork/CLI 동기화 2026-07-29 14:27
- 66d3abefa auto: Cowork/CLI 동기화 2026-07-29 14:27
- 42263f1ae auto: Cowork/CLI 동기화 2026-07-29 14:27
- 8bf252be5 auto: Cowork/CLI 동기화 2026-07-29 14:22
- c0c25ce63 auto: Cowork/CLI 동기화 2026-07-29 14:22
- ec9bdab73 auto: Cowork/CLI 동기화 2026-07-29 14:22
- 196f9b0ac auto: Cowork/CLI 동기화 2026-07-29 14:17
- 691ef5991 auto: Cowork/CLI 동기화 2026-07-29 14:17
- 0a0fe7f86 auto: Cowork/CLI 동기화 2026-07-29 14:17
- 2213c0eea auto: Cowork/CLI 동기화 2026-07-29 14:12
- 1a57ad64b auto: Cowork/CLI 동기화 2026-07-29 14:12
- 373b473b6 auto: Cowork/CLI 동기화 2026-07-29 14:12
- 5dfbe3208 auto: Cowork/CLI 동기화 2026-07-29 14:08
- e585d7cd9 auto: Cowork/CLI 동기화 2026-07-29 14:08
- c58866a89 auto: Cowork/CLI 동기화 2026-07-29 14:07
- dbaf3950e auto: Cowork/CLI 동기화 2026-07-29 14:07
- 3169145a5 auto: Cowork/CLI 동기화 2026-07-29 14:07
- 31ae8d95d auto: Cowork/CLI 동기화 2026-07-29 14:02
- 0af44909c auto: Cowork/CLI 동기화 2026-07-29 14:02
- 5f28cd644 auto: Cowork/CLI 동기화 2026-07-29 14:02
- bcae2def5 auto: Cowork/CLI 동기화 2026-07-29 13:57
- 5a806487e auto: Cowork/CLI 동기화 2026-07-29 13:57
- 1fe607bcc auto: Cowork/CLI 동기화 2026-07-29 13:57
- f4dd14fa0 auto: Cowork/CLI 동기화 2026-07-29 13:52
- 586b9d908 auto: Cowork/CLI 동기화 2026-07-29 13:52
- 6566c38b9 auto: Cowork/CLI 동기화 2026-07-29 13:52
- 37dbe66ff auto: Cowork/CLI 동기화 2026-07-29 13:47
- ba6a8bee3 auto: Cowork/CLI 동기화 2026-07-29 13:47
- 7db3a379b auto: Cowork/CLI 동기화 2026-07-29 13:47
- a0f442c7f auto: Cowork/CLI 동기화 2026-07-29 13:42
- 0b9576cdb auto: Cowork/CLI 동기화 2026-07-29 13:42
- f729277ef auto: Cowork/CLI 동기화 2026-07-29 13:42
- 8d522c33c auto: Cowork/CLI 동기화 2026-07-29 13:37
- 769a3de52 auto: Cowork/CLI 동기화 2026-07-29 13:37
- fb695620f auto: Cowork/CLI 동기화 2026-07-29 13:37
- 2a63f0650 auto: Cowork/CLI 동기화 2026-07-29 13:32
- 228be7770 auto: Cowork/CLI 동기화 2026-07-29 13:32
- bfc9f6242 auto: Cowork/CLI 동기화 2026-07-29 13:32
- 9da659a69 auto: Cowork/CLI 동기화 2026-07-29 13:27
- 466d7dcde auto: Cowork/CLI 동기화 2026-07-29 13:27
- ae10e660c auto: Cowork/CLI 동기화 2026-07-29 13:27
- 776363391 auto: Cowork/CLI 동기화 2026-07-29 13:22
- 5525c7a33 auto: Cowork/CLI 동기화 2026-07-29 13:22
- 97cbb5ebe auto: Cowork/CLI 동기화 2026-07-29 13:22
- afad018d0 auto: Cowork/CLI 동기화 2026-07-29 13:17
- fafab169c auto: Cowork/CLI 동기화 2026-07-29 13:17
- 80532c9e3 auto: Cowork/CLI 동기화 2026-07-29 13:17
- d148395ea auto: Cowork/CLI 동기화 2026-07-29 13:12
- b9e3f53c1 auto: Cowork/CLI 동기화 2026-07-29 13:12
- e45d041e8 auto: Cowork/CLI 동기화 2026-07-29 13:12
- 034886261 auto: Cowork/CLI 동기화 2026-07-29 13:07
- f8e853bc6 auto: Cowork/CLI 동기화 2026-07-29 13:07
- 252d234d9 auto: Cowork/CLI 동기화 2026-07-29 13:07
- 9a66b5380 auto: Cowork/CLI 동기화 2026-07-29 13:02
- 64352222e auto: Cowork/CLI 동기화 2026-07-29 13:02
- e5b9fb924 auto: Cowork/CLI 동기화 2026-07-29 13:02
- 476296f0f auto: Cowork/CLI 동기화 2026-07-29 12:57
- 25f72dba8 auto: Cowork/CLI 동기화 2026-07-29 12:57
- 1c16ec0dd auto: Cowork/CLI 동기화 2026-07-29 12:57
- f88cc067f auto: Cowork/CLI 동기화 2026-07-29 12:52
- 83b435bcd auto: Cowork/CLI 동기화 2026-07-29 12:52
- bc1364d19 auto: Cowork/CLI 동기화 2026-07-29 12:52
- b54f98257 auto: Cowork/CLI 동기화 2026-07-29 12:47
- c7d55b549 auto: Cowork/CLI 동기화 2026-07-29 12:47
- f5a5511ae auto: Cowork/CLI 동기화 2026-07-29 12:47
- 96dc78ef5 auto: Cowork/CLI 동기화 2026-07-29 12:42
- e18078c97 auto: Cowork/CLI 동기화 2026-07-29 12:42
- 18c3dd816 auto: Cowork/CLI 동기화 2026-07-29 12:42
- b9cde1457 auto: Cowork/CLI 동기화 2026-07-29 12:37
- 5e84ac4c7 auto: Cowork/CLI 동기화 2026-07-29 12:37
- 25c76071f auto: Cowork/CLI 동기화 2026-07-29 12:37
- 91b1373f9 auto: Cowork/CLI 동기화 2026-07-29 12:32
- d28b9693a auto: Cowork/CLI 동기화 2026-07-29 12:32
- 6510a2a75 auto: Cowork/CLI 동기화 2026-07-29 12:32
- f8e77f432 auto: Cowork/CLI 동기화 2026-07-29 12:27
- 31b9f6384 auto: Cowork/CLI 동기화 2026-07-29 12:27
- 527ae5eca auto: Cowork/CLI 동기화 2026-07-29 12:26
- 826689343 auto: Cowork/CLI 동기화 2026-07-29 12:22
- 774d3b6a8 auto: Cowork/CLI 동기화 2026-07-29 12:22
- aa7004fcb auto: Cowork/CLI 동기화 2026-07-29 12:21
- 965d808e1 auto: Cowork/CLI 동기화 2026-07-29 12:17
- 0b2d86122 auto: Cowork/CLI 동기화 2026-07-29 12:16
- 31a91742b auto: Cowork/CLI 동기화 2026-07-29 12:12
- a76d8739c auto: Cowork/CLI 동기화 2026-07-29 12:11
- 4e854fb10 auto: Cowork/CLI 동기화 2026-07-29 12:08
- bd375d9c3 auto: Cowork/CLI 동기화 2026-07-29 12:08
- f53cd8f14 auto: Cowork/CLI 동기화 2026-07-29 12:07
- 75d3a0883 auto: Cowork/CLI 동기화 2026-07-29 12:06
- efa49238f auto: Cowork/CLI 동기화 2026-07-29 12:02
- 9b087b79a auto: Cowork/CLI 동기화 2026-07-29 12:01
- cd0e0c07c auto: Cowork/CLI 동기화 2026-07-29 11:57
- e1b7559b6 auto: Cowork/CLI 동기화 2026-07-29 11:56
- 9d3c697c8 auto: Cowork/CLI 동기화 2026-07-29 11:52
- 848611971 auto: Cowork/CLI 동기화 2026-07-29 11:51
- ab20be2e0 auto: Cowork/CLI 동기화 2026-07-29 11:47
- 3e14dde32 auto: Cowork/CLI 동기화 2026-07-29 11:46
- 3be4ca5e0 auto: Cowork/CLI 동기화 2026-07-29 11:42
- aaa127b97 auto: Cowork/CLI 동기화 2026-07-29 11:41
- 91b64a04b auto: Cowork/CLI 동기화 2026-07-29 11:37
- fa8779152 auto: Cowork/CLI 동기화 2026-07-29 11:36
- 834c4584f auto: Cowork/CLI 동기화 2026-07-29 11:32
- 6d94d3e40 auto: Cowork/CLI 동기화 2026-07-29 11:31
- f69f17e25 auto: Cowork/CLI 동기화 2026-07-29 11:27
- 8240c4b76 auto: Cowork/CLI 동기화 2026-07-29 11:26
- 7885c59d8 auto: Cowork/CLI 동기화 2026-07-29 11:22
- 8d8c5d7ec auto: Cowork/CLI 동기화 2026-07-29 11:21
- 6e15e0747 auto: Cowork/CLI 동기화 2026-07-29 11:17
- ecc39b4be auto: Cowork/CLI 동기화 2026-07-29 11:16
- b0895fe2d auto: Cowork/CLI 동기화 2026-07-29 11:12
- c7152ced7 auto: Cowork/CLI 동기화 2026-07-29 11:11
- fa3bc6085 auto: Cowork/CLI 동기화 2026-07-29 11:07
- f6b31d8b0 auto: Cowork/CLI 동기화 2026-07-29 11:06
- 0ca3fd1d0 auto: Cowork/CLI 동기화 2026-07-29 11:02
- 44111515d auto: Cowork/CLI 동기화 2026-07-29 11:01
- ce825ad24 auto: Cowork/CLI 동기화 2026-07-29 10:57
- ec9f11136 auto: Cowork/CLI 동기화 2026-07-29 10:56
- ba88c8621 auto: Cowork/CLI 동기화 2026-07-29 10:52
- 7d6c73025 auto: Cowork/CLI 동기화 2026-07-29 10:51
- 6d733ed07 auto: Cowork/CLI 동기화 2026-07-29 10:47
- 20ade59c6 auto: Cowork/CLI 동기화 2026-07-29 10:46
- e6b07c5d1 auto: Cowork/CLI 동기화 2026-07-29 10:42
- e645446b2 auto: Cowork/CLI 동기화 2026-07-29 10:41
- 93152e284 auto: Cowork/CLI 동기화 2026-07-29 10:37
- a8fdeacfb auto: Cowork/CLI 동기화 2026-07-29 10:36
- 7a1ed4544 auto: Cowork/CLI 동기화 2026-07-29 10:32
- df5efd777 auto: Cowork/CLI 동기화 2026-07-29 10:31
- d8f3ff42a auto: Cowork/CLI 동기화 2026-07-29 10:27
- bc9d71bea auto: Cowork/CLI 동기화 2026-07-29 10:26
- 99799697f auto: Cowork/CLI 동기화 2026-07-29 10:22
- 2d1adc29a auto: Cowork/CLI 동기화 2026-07-29 10:21
- 1993f1b54 auto: Cowork/CLI 동기화 2026-07-29 10:17
- d5df4dfa0 auto: Cowork/CLI 동기화 2026-07-29 10:16
- 9b25c5fb8 auto: Cowork/CLI 동기화 2026-07-29 10:12
- 76195a3ef auto: Cowork/CLI 동기화 2026-07-29 10:11
- 85d7e7e3f auto: Cowork/CLI 동기화 2026-07-29 10:08
- 56923b35c auto: Cowork/CLI 동기화 2026-07-29 10:08
- df22f1359 auto: Cowork/CLI 동기화 2026-07-29 10:07
- ca8270070 auto: Cowork/CLI 동기화 2026-07-29 10:06
- 6649ea085 auto: Cowork/CLI 동기화 2026-07-29 10:02
- 9964f50fe auto: Cowork/CLI 동기화 2026-07-29 10:01
- 03274a253 auto: Cowork/CLI 동기화 2026-07-29 09:57
- 72aa29c0c auto: Cowork/CLI 동기화 2026-07-29 09:56
- 468251ebf auto: Cowork/CLI 동기화 2026-07-29 09:52
- a820179be auto: Cowork/CLI 동기화 2026-07-29 09:51
- a1c8cf2f8 auto: Cowork/CLI 동기화 2026-07-29 09:47
- aaa6ea520 auto: Cowork/CLI 동기화 2026-07-29 09:46
- 116fc2d34 auto: Cowork/CLI 동기화 2026-07-29 09:42
- 915f006fd auto: Cowork/CLI 동기화 2026-07-29 09:41
- d92d4b4be auto: Cowork/CLI 동기화 2026-07-29 09:37
- 2cb630379 auto: Cowork/CLI 동기화 2026-07-29 09:36
- f3db7da0a auto: Cowork/CLI 동기화 2026-07-29 09:32
- a3d0a52b3 auto: Cowork/CLI 동기화 2026-07-29 09:31
- 77b9a7280 auto: Cowork/CLI 동기화 2026-07-29 09:27
- 91943b47a auto: Cowork/CLI 동기화 2026-07-29 09:26
- 9385464ca auto: Cowork/CLI 동기화 2026-07-29 09:22
- 741ef46dd auto: Cowork/CLI 동기화 2026-07-29 09:21
- 53c93c80c auto: Cowork/CLI 동기화 2026-07-29 09:17
- c9b530494 auto: Cowork/CLI 동기화 2026-07-29 09:16
- b823ae157 auto: Cowork/CLI 동기화 2026-07-29 09:12
- 464681284 auto: Cowork/CLI 동기화 2026-07-29 09:11
- ca08c8f9a auto: Cowork/CLI 동기화 2026-07-29 09:07
- 59c9463b6 auto: Cowork/CLI 동기화 2026-07-29 09:06
- 84f393340 auto: Cowork/CLI 동기화 2026-07-29 09:02
- 9910d9afd auto: Cowork/CLI 동기화 2026-07-29 09:01
- 98a0f2cde auto: Cowork/CLI 동기화 2026-07-29 08:57
- 928290343 auto: Cowork/CLI 동기화 2026-07-29 08:56
- 5bc402132 auto: Cowork/CLI 동기화 2026-07-29 08:52
- 161d060f2 auto: Cowork/CLI 동기화 2026-07-29 08:51
- 74cdcfefe auto: Cowork/CLI 동기화 2026-07-29 08:47
- 247c408f1 auto: Cowork/CLI 동기화 2026-07-29 08:46
- f474966be auto: Cowork/CLI 동기화 2026-07-29 08:42
- cea7a55e7 auto: Cowork/CLI 동기화 2026-07-29 08:41
- b81c0c798 auto: Cowork/CLI 동기화 2026-07-29 08:37
- 9310c8a06 auto: Cowork/CLI 동기화 2026-07-29 08:36
- af3b7450a auto: Cowork/CLI 동기화 2026-07-29 08:32
- 3f0fab888 auto: Cowork/CLI 동기화 2026-07-29 08:31
- bc63067e4 auto: Cowork/CLI 동기화 2026-07-29 08:27
- 16364524a auto: Cowork/CLI 동기화 2026-07-29 08:26
- ba9fc757a auto: Cowork/CLI 동기화 2026-07-29 08:22
- 4f11d2159 auto: Cowork/CLI 동기화 2026-07-29 08:21
- 42c99251e auto: Cowork/CLI 동기화 2026-07-29 08:17
- 40fda6275 auto: Cowork/CLI 동기화 2026-07-29 08:16
- 686f583c7 auto: Cowork/CLI 동기화 2026-07-29 08:12
- 5d349fa10 auto: Cowork/CLI 동기화 2026-07-29 08:11
- e8769c7ed auto: Cowork/CLI 동기화 2026-07-29 08:08
- 3bc775e1c auto: Cowork/CLI 동기화 2026-07-29 08:08
- 820b6caaa auto: Cowork/CLI 동기화 2026-07-29 08:07
- bb16649a6 auto: Cowork/CLI 동기화 2026-07-29 08:06
- 0fc2c7bee auto: Cowork/CLI 동기화 2026-07-29 08:02
- fd084a149 auto: Cowork/CLI 동기화 2026-07-29 08:01
- 7cf6b4945 auto: Cowork/CLI 동기화 2026-07-29 08:00
- b25797bf6 auto: Cowork/CLI 동기화 2026-07-29 07:57
- e32098047 auto: Cowork/CLI 동기화 2026-07-29 07:56
- 3d7b93bd6 auto: Cowork/CLI 동기화 2026-07-29 07:52
- 059f0bab5 auto: Cowork/CLI 동기화 2026-07-29 07:51
- 0e93c90a8 auto: Cowork/CLI 동기화 2026-07-29 07:47
- 72feaa25f auto: Cowork/CLI 동기화 2026-07-29 07:46
- 4cece5f6d auto: Cowork/CLI 동기화 2026-07-29 07:42
- 4025f2a3e auto: Cowork/CLI 동기화 2026-07-29 07:41
- 99714c945 auto: Cowork/CLI 동기화 2026-07-29 07:37
- caf9916aa auto: Cowork/CLI 동기화 2026-07-29 07:36
- 0946e75b0 auto: Cowork/CLI 동기화 2026-07-29 07:32
- 2e5435319 auto: Cowork/CLI 동기화 2026-07-29 07:31
- 9dc4dd533 auto: Cowork/CLI 동기화 2026-07-29 07:27
- 0afdbb76a auto: Cowork/CLI 동기화 2026-07-29 07:26
- 38d63c5fd auto: Cowork/CLI 동기화 2026-07-29 07:22
- a9cb8a82b auto: Cowork/CLI 동기화 2026-07-29 07:21
- 6688ffd68 auto: Cowork/CLI 동기화 2026-07-29 07:17
- cafc63b5f auto: Cowork/CLI 동기화 2026-07-29 07:16
- b2e9c46ab auto: Cowork/CLI 동기화 2026-07-29 07:12
- 18b7cabf1 auto: Cowork/CLI 동기화 2026-07-29 07:11
- 83146aab9 auto: Cowork/CLI 동기화 2026-07-29 07:07
- 66d71f193 auto: Cowork/CLI 동기화 2026-07-29 07:06
- 31ecf17d4 auto: Cowork/CLI 동기화 2026-07-29 07:02
- c60123b54 auto: Cowork/CLI 동기화 2026-07-29 07:01
- 7000185ad auto: Cowork/CLI 동기화 2026-07-29 06:57
- 7eb9a6736 auto: Cowork/CLI 동기화 2026-07-29 06:56
- 7135c6b36 auto: Cowork/CLI 동기화 2026-07-29 06:52
- 8d4073227 auto: Cowork/CLI 동기화 2026-07-29 06:51
- 00c02336e auto: Cowork/CLI 동기화 2026-07-29 06:47
- 226eaf87f auto: Cowork/CLI 동기화 2026-07-29 06:46
- 91a87c2f0 auto: Cowork/CLI 동기화 2026-07-29 06:42
- 32faffb78 auto: Cowork/CLI 동기화 2026-07-29 06:41
- 70aa96e6f auto: Cowork/CLI 동기화 2026-07-29 06:37
- d88cd0590 auto: Cowork/CLI 동기화 2026-07-29 06:36
- 06f606583 auto: Cowork/CLI 동기화 2026-07-29 06:32
- 7ab4a73d4 auto: Cowork/CLI 동기화 2026-07-29 06:31
- 360d913bc auto: Cowork/CLI 동기화 2026-07-29 06:27
- 0547b339e auto: Cowork/CLI 동기화 2026-07-29 06:26
- 49bb3a40b auto: Cowork/CLI 동기화 2026-07-29 06:22
- 411701b74 auto: Cowork/CLI 동기화 2026-07-29 06:21
- 74804a8d2 auto: Cowork/CLI 동기화 2026-07-29 06:17
- a27eb600b auto: Cowork/CLI 동기화 2026-07-29 06:16
- 7c60b0bf9 auto: Cowork/CLI 동기화 2026-07-29 06:12
- 419322f3c auto: Cowork/CLI 동기화 2026-07-29 06:11
- da92e57df auto: Cowork/CLI 동기화 2026-07-29 06:08
- ca6525316 auto: Cowork/CLI 동기화 2026-07-29 06:08
- 286c998ef auto: Cowork/CLI 동기화 2026-07-29 06:07
- 6d8032420 auto: Cowork/CLI 동기화 2026-07-29 06:06
- 48800c923 auto: Cowork/CLI 동기화 2026-07-29 06:02
- 767ac017d auto: Cowork/CLI 동기화 2026-07-29 06:01
- a62c694f9 auto: Cowork/CLI 동기화 2026-07-29 05:47
- ae7d4cf12 auto: Cowork/CLI 동기화 2026-07-29 05:46
- b209a2a49 auto: Cowork/CLI 동기화 2026-07-29 05:32
- 30097645a auto: Cowork/CLI 동기화 2026-07-29 05:31
- ef31b88af auto: Cowork/CLI 동기화 2026-07-29 05:17
- 07139417c auto: Cowork/CLI 동기화 2026-07-29 05:16
- 5adaf4f41 auto: Cowork/CLI 동기화 2026-07-29 05:02
- 3cdc7479f auto: Cowork/CLI 동기화 2026-07-29 05:01
- 2a344e415 auto: Cowork/CLI 동기화 2026-07-29 04:47
- 9e5074380 auto: Cowork/CLI 동기화 2026-07-29 04:46
- 04b07a31e auto: Cowork/CLI 동기화 2026-07-29 04:32
- 3bc0e68ae auto: Cowork/CLI 동기화 2026-07-29 04:31
- 3d7f2a815 auto: Cowork/CLI 동기화 2026-07-29 04:17
- 731f8d4c5 auto: Cowork/CLI 동기화 2026-07-29 04:16
- d63760e52 auto: Cowork/CLI 동기화 2026-07-29 04:08
- 2f13d8169 auto: Cowork/CLI 동기화 2026-07-29 04:08
- e400aae37 auto: Cowork/CLI 동기화 2026-07-29 04:02
- 043a469fb auto: Cowork/CLI 동기화 2026-07-29 04:01
- 628cb7974 auto: Cowork/CLI 동기화 2026-07-29 03:47
- efc15113a auto: Cowork/CLI 동기화 2026-07-29 03:46
- 8abc2e615 auto: Cowork/CLI 동기화 2026-07-29 03:32
- 0e9f903ce auto: Cowork/CLI 동기화 2026-07-29 03:31
- 4e33cb13b auto: Cowork/CLI 동기화 2026-07-29 03:17
- 1d0dc42db auto: Cowork/CLI 동기화 2026-07-29 03:16
- fa51626f5 auto: Cowork/CLI 동기화 2026-07-29 03:02
- 2bfde1f2f auto: Cowork/CLI 동기화 2026-07-29 03:01
- 8ccb4f1d6 auto: Cowork/CLI 동기화 2026-07-29 02:47
- 962fa1ebc auto: Cowork/CLI 동기화 2026-07-29 02:46
- b9f5feb03 auto: Cowork/CLI 동기화 2026-07-29 02:32
- d2ea74a2e auto: Cowork/CLI 동기화 2026-07-29 02:31
- dc74e73fb auto: Cowork/CLI 동기화 2026-07-29 02:17
- f0dd6070b auto: Cowork/CLI 동기화 2026-07-29 02:16
- d9ff3765f auto: Cowork/CLI 동기화 2026-07-29 02:08
- 77601760d auto: Cowork/CLI 동기화 2026-07-29 02:08
- 096ae8a1d auto: Cowork/CLI 동기화 2026-07-29 02:02
- 5ef94516d auto: Cowork/CLI 동기화 2026-07-29 02:01
- bd2776619 auto: Cowork/CLI 동기화 2026-07-29 01:57
- 4463c09af auto: Cowork/CLI 동기화 2026-07-29 01:56
- e9892d976 auto: Cowork/CLI 동기화 2026-07-29 01:52
- e91dd6cd4 auto: Cowork/CLI 동기화 2026-07-29 01:51
- 1cb7bf981 auto: Cowork/CLI 동기화 2026-07-29 01:47
- 914224ff4 auto: Cowork/CLI 동기화 2026-07-29 01:46
- 255c9cf32 auto: Cowork/CLI 동기화 2026-07-29 01:42
- cdbf51346 auto: Cowork/CLI 동기화 2026-07-29 01:41
- 7c7dd1ebd auto: Cowork/CLI 동기화 2026-07-29 01:37
- 074aceb06 auto: Cowork/CLI 동기화 2026-07-29 01:36
- ac5dd81f5 auto: Cowork/CLI 동기화 2026-07-29 01:32
- c33e790db auto: Cowork/CLI 동기화 2026-07-29 01:31
- f9524ea53 auto: Cowork/CLI 동기화 2026-07-29 01:27
- bfd3a7d71 auto: Cowork/CLI 동기화 2026-07-29 01:26
- d3ab72e27 auto: Cowork/CLI 동기화 2026-07-29 01:22
- 2c6834ca6 auto: Cowork/CLI 동기화 2026-07-29 01:21
- 1346d97d4 auto: Cowork/CLI 동기화 2026-07-29 01:17
- 44433805c auto: Cowork/CLI 동기화 2026-07-29 01:16
- e754bd36d auto: Cowork/CLI 동기화 2026-07-29 01:12
- ec8ea48b2 auto: Cowork/CLI 동기화 2026-07-29 01:11
- b53e7e548 auto: Cowork/CLI 동기화 2026-07-29 01:07
- 10ee4686f auto: Cowork/CLI 동기화 2026-07-29 01:06
- 047c83f29 auto: Cowork/CLI 동기화 2026-07-29 01:02
- e2beca976 auto: Cowork/CLI 동기화 2026-07-29 01:01
- eae5ca194 auto: Cowork/CLI 동기화 2026-07-29 00:57
- 9eda2c627 auto: Cowork/CLI 동기화 2026-07-29 00:56
- 68f43e616 auto: Cowork/CLI 동기화 2026-07-29 00:52
- 5319d0280 auto: Cowork/CLI 동기화 2026-07-29 00:51
- 0e9e67d30 auto: Cowork/CLI 동기화 2026-07-29 00:47
- 9ae7c4c44 auto: Cowork/CLI 동기화 2026-07-29 00:46
- 2e5f26a54 auto: Cowork/CLI 동기화 2026-07-29 00:42
- 6ed04be8d auto: Cowork/CLI 동기화 2026-07-29 00:41
- 99f41554c auto: Cowork/CLI 동기화 2026-07-29 00:37
- 6cec7c282 auto: Cowork/CLI 동기화 2026-07-29 00:36
- 97a13e1b9 auto: Cowork/CLI 동기화 2026-07-29 00:32
- 4259a2dfc auto: Cowork/CLI 동기화 2026-07-29 00:31
- bda2c29ba auto: Cowork/CLI 동기화 2026-07-29 00:27
- 04cb4b193 auto: Cowork/CLI 동기화 2026-07-29 00:26
- 937c663df auto: Cowork/CLI 동기화 2026-07-29 00:22
- a1fa33b64 auto: Cowork/CLI 동기화 2026-07-29 00:21
- b196038d5 auto: Cowork/CLI 동기화 2026-07-29 00:17
- f1bf67ced auto: Cowork/CLI 동기화 2026-07-29 00:16
- 644f587fd auto: Cowork/CLI 동기화 2026-07-29 00:12
- 39d450cf5 auto: Cowork/CLI 동기화 2026-07-29 00:11
- 067bcff27 auto: Cowork/CLI 동기화 2026-07-29 00:08
- 3ca4987ab auto: Cowork/CLI 동기화 2026-07-29 00:08
- 8163b5291 auto: Cowork/CLI 동기화 2026-07-29 00:07
- 7277549bb auto: Cowork/CLI 동기화 2026-07-29 00:06
- 24ef701b2 auto: Cowork/CLI 동기화 2026-07-29 00:02
- fc7e48cb0 auto: Cowork/CLI 동기화 2026-07-29 00:01

---

## 다음 할 일 (각 프로젝트 REF 기반)

- **260620_3_Multimedia_summary** ? — ✅ 배포 완료 · ✅ APK 설치 완료 · ✅ 통합 테스트 성공
- **260623_1_study_all** v1.0 — ?
- **260625_1_n8n_finance** v1.1 (신기술 적용 완료) — n8n v1.123.63 Active (포트 5680) ✅ — GeekNews 파이프라인 + 텔레그램 inbound 모두 정상 작동

---

## 호칭 안내
| 호칭 | 대상 |
|------|------|
| **만복이** | Claude Code CLI (데스크탑 메인 세션) |
| **코니** | Cowork AI (Remote Control 세션, 지금 이 세션) |
| **일복이, 이복이, 삼복이...** | 서브에이전트 (만복이의 쫄개들) |

---

## 코니 안내
- 전역 지시사항: `C:\Users\82102\.claude\CLAUDE.md`
- 세션 브릿지:   `D:\AI\CLAUDE.md`
- 만복2 오늘 요약: `D:\AI\TEMP_MANBOK\만복2_오늘정리_20260729.md`