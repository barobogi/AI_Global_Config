# 코니 Quick Sync — 2026-08-20 09:16
> 이 파일만 붙여넣으면 동기화 완료. 상세 커밋: 코니_sync.md

## 프로젝트 현황
- **260620_3_Multimedia_summary** ? — ✅ 배포 완료 · ✅ APK 설치 완료 · ✅ 통합 테스트 성공
- **260623_1_study_all** v1.0 — ?
- **260625_1_n8n_finance** v1.1 (신기술 적용 완료) — n8n v1.123.63 Active (포트 5680) ✅ — GeekNews 파이프라인 + 텔레그램 inb
## 📜 코니 담당 활성 규칙 (rule_governance_db)
- [J-01_PUSH_ALL] 3AI 동시 격발 규정: 메시지 발송 직후 반드시 push_to_all.py를 실행하여 3AI 전원을 동시 격발할 것.
- [J-02_CC_RULE] 메시지 CC 최소화: 불필요한 노이즈 방지를 위해 필요한 시점에만 CC를 걸고 순차적으로 전달할 것.
- [J-03_REPORT_FORMAT] 과제 완료보고 표준: 보고서 최상단에 [완료보고] Task ID와 핵심 내용을 명확히 포함할 것.
- [J-04_GPS_CHECK] GPS 지시서 필수 구조: G(Goal), P(Proof), S(Steps) 3대 항목 및 정량적 완료 증거를 첨부할 것.
- [J-05_TASK_ARCHIVE] Task Archive 보관: 3차 이상 장기 태스크는 task_archives/T0XX/ 폴더에 단계별 분리 보관할 것.
- [J-06_SKILL_EVAL] 스킬 Eval 의무화: 신규 스킬 제안 시 SKILL.md, 5개 이상 테스트케이스, 정량 채점 기준을 필수 동봉할 것.
- [J-07_PRE_ROOT_ASSIGN] 신규 프로젝트 뿌리체계 사전 편입: 신규 기능 생성 전 만복(PM)에게 뿌리 편입 제안서를 먼저 보내 승인을 득할 것.
- [J-08_README_4STD] 43_function_dev 4대 표준 README: 개요, 사용법, 3AI 연결점, 추가 확장 아이디어 및 3AI 의견란을 필수로 작성할 것.
- [J-09_PARALLEL_SEARCH] Genspark 병렬 리서치 공통 규정: 방대한 리서치 시 반드시 parallel_search.py 다중 키워드 병렬 검색을 활용할 것.
- [J-10_CONCEPT_CARD] 개념카드 작성 원칙: 저장 전 '나중에 AI에게 무엇을 물어볼 것인가' 활용 시나리오를 먼저 명시할 것.
- [J-11_DIARY_FLOW] 일일 다이어리 단일 위치 및 순서: diaries/YYYYMMDD_3AI_일일다이어리.md 단일 파일에 코니➔안티➔만복 순서로 작성할 것.
- [J-12_TRIPLE_CHECK] 업무 착수 전 3중 교차 검증: inbox.md, 당일 일정 파일, 전담 워크스페이스를 대조하여 본인 담당 업무를 정확히 식별할 것.
- [H-01_ZERO_SIMULATION] 모의 대화/사칭 대필 절대 금지: 타 AI 본체가 직접 발화하지 않은 모의/대필 데이터를 절대 실제 발언으로 포장하지 말 것.
- [H-02_USER_APPROVAL_GATE] 선보고 후승인 원칙: 타 AI 인계 전 반드시 바로보기님의 명시적 승인을 득할 것.
- [H-03_ROOT_FOLDER_PROTECT] D:\AI 루트 폴더 생성 금지: D:\AI 최상위에는 뿌리체계 프로젝트 폴더 외 임의 산출물 생성을 엄금할 것.
- [K-01_TASKS_CHECK_BOOT] 세션 시작 tasks.json 필수 확인: 지시를 기다리지 말고 tasks.json에서 코니 담당 in_progress/pending 항목을 먼저 착수할 것.
- [K-02_AUDITOR_TASTE] Auditor 심미안 및 확정 기획안 실대조: 인상 비평을 지양하고 확정 기획서 항목과 1:1 정밀 대조하여 검증 책임을 명시할 것.
- [K-03_NO_TYPO_COPY] 한글 파일명 수동 재입력 금지: 오타 방지를 위해 파일 경로는 직전 조회 결과에서 100% 복사하여 사용할 것.
- [K-04_VIDEO_TEXT_QA] 유튜브 검증 2차 텍스트 집중: 대본, 자막 싱크, 오타, 메시지 일관성을 집중 검증할 것.
