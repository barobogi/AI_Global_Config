# 코니 세션 싱크 파일
**자동 생성**: 2026-08-29 19:03 (master_watch.py)
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
- 0fb2ae9 auto: Cowork/CLI 동기화 2026-08-29 19:00
- 3d5d218 auto: 현재가 갱신 2026-08-29T18:00 현재가:35개
- f843b7d auto: 현재가 갱신 2026-08-29T12:00 현재가:35개
- ed10cca auto: 현재가 갱신 2026-08-29T06:00 현재가:35개

**Daily_for_Barobogi**
- 186a8bc auto: Cowork/CLI 동기화 2026-08-29 18:00
- 80fae3f auto: Cowork/CLI 동기화 2026-08-29 12:00
- dd4d922 auto: Cowork/CLI 동기화 2026-08-29 06:10
- 0057d92 auto: Cowork/CLI 동기화 2026-08-29 06:09
- c81a60a auto: Cowork/CLI 동기화 2026-08-29 06:00

**AI_Global_Config**
- 9a86ad97a docs: SESSION_LOG 8/29 세션 갱신, 8/20 항목 아카이브 이관
- 8a477b223 auto: Cowork/CLI 동기화 2026-08-29 04:00
- a8a35dd44 auto: Cowork/CLI 동기화 2026-08-29 04:47
- 13a557627 auto: Cowork/CLI 동기화 2026-08-29 04:01
- 74b8aa685 fix: 오늘뭐하지 hard_filter N째주 휴무 판정 순서 버그 수정 + 배포 인프라 추가
- cb7eb69c6 auto: Cowork/CLI 동기화 2026-08-29 02:48
- a87154fa3 auto: Cowork/CLI 동기화 2026-08-29 00:47
- 993ad7bae auto: Cowork/CLI 동기화 2026-08-29 00:43
- 2329d81df auto: Cowork/CLI 동기화 2026-08-29 00:37
- e36344619 auto: Cowork/CLI 동기화 2026-08-29 00:33
- c5e007571 auto: Cowork/CLI 동기화 2026-08-29 00:27
- cb51aff66 auto: Cowork/CLI 동기화 2026-08-29 00:23
- 9cbf53c5b auto: Cowork/CLI 동기화 2026-08-29 00:17
- c11d6138a auto: Cowork/CLI 동기화 2026-08-29 00:13
- 547d3fe95 auto: Cowork/CLI 동기화 2026-08-29 00:07
- 3b6ce4f0f auto: Cowork/CLI 동기화 2026-08-29 00:03

**Global_Define**
- f74ddfc feat: 재발방지 2종 — 대용량파일 커밋가드 + 일일 git gc

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
- 만복2 오늘 요약: `D:\AI\TEMP_MANBOK\만복2_오늘정리_20260829.md`