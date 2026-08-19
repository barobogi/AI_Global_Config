# 코니 세션 싱크 파일
**자동 생성**: 2026-08-18 23:48 (master_watch.py)
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
- a1934b8 auto: Cowork/CLI 동기화 2026-08-18 19:01

**Daily_for_Barobogi**
- a5d8563 auto: Cowork/CLI 동기화 2026-08-18 22:09
- c85ef60 auto: Cowork/CLI 동기화 2026-08-18 22:08
- 10ab49c auto: Cowork/CLI 동기화 2026-08-18 19:07
- a6ca87f auto: Cowork/CLI 동기화 2026-08-18 09:06
- a7066d5 auto: Cowork/CLI 동기화 2026-08-18 08:05
- 57ed940 auto: Cowork/CLI 동기화 2026-08-18 08:00
- f915fef auto: Cowork/CLI 동기화 2026-08-18 06:05
- 87da4c8 auto: Cowork/CLI 동기화 2026-08-18 06:04
- efcab49 auto: Cowork/CLI 동기화 2026-08-18 04:03
- 683e31c auto: Cowork/CLI 동기화 2026-08-18 02:03

**AI_Global_Config**
- b21a6938d T066 실적용 2단계: C-1~5 헌법급 규칙을 CLAUDE.md로 이관
- b0bec8973 T066 실적용 1단계: AGENTS.md 체크리스트 규칙 12개 DB 이관 + push_to_all.py JIT 연동

**Global_Define**
- bda739d auto: Cowork/CLI 동기화 2026-08-18 23:48
- 8e050e2 auto: Cowork/CLI 동기화 2026-08-18 23:41
- 794e44c auto: Cowork/CLI 동기화 2026-08-18 23:39
- b602f11 auto: Cowork/CLI 동기화 2026-08-18 23:18

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
- 만복2 오늘 요약: `D:\AI\TEMP_MANBOK\만복2_오늘정리_20260818.md`