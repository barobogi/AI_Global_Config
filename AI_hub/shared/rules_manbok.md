# 📜 3AI 활성 규칙 스냅샷 (MANBOK)
> 자동 생성/동기화: `43_function_dev/02_rule_governance_db/rule_governance.db` (2026-08-30 22:06)
> 용도: MANBOK 직접 조회용 JIT 규칙 스냅샷

| ID | 규칙명 | 대상 | Trigger Tag | 본문 |
| :--- | :--- | :---: | :---: | :--- |
| `J-01_PUSH_ALL` | **3AI 동시 격발 규정** | `all` | `before_send` | 메시지 발송 직후 반드시 push_to_all.py를 실행하여 3AI 전원을 동시 격발할 것. |
| `J-02_CC_RULE` | **메시지 CC 최소화** | `all` | `before_send` | 불필요한 노이즈 방지를 위해 필요한 시점에만 CC를 걸고 순차적으로 전달할 것. |
| `J-03_REPORT_FORMAT` | **과제 완료보고 표준** | `all` | `before_complete` | 보고서 최상단에 [완료보고] Task ID와 핵심 내용을 명확히 포함할 것. |
| `J-04_GPS_CHECK` | **GPS 지시서 필수 구조** | `all` | `before_complete` | G(Goal), P(Proof), S(Steps) 3대 항목 및 정량적 완료 증거를 첨부할 것. |
| `J-05_TASK_ARCHIVE` | **Task Archive 보관** | `all` | `before_complete` | 3차 이상 장기 태스크는 task_archives/T0XX/ 폴더에 단계별 분리 보관할 것. |
| `J-06_SKILL_EVAL` | **스킬 Eval 의무화** | `all` | `before_skill` | 신규 스킬 제안 시 SKILL.md, 5개 이상 테스트케이스, 정량 채점 기준을 필수 동봉할 것. |
| `J-07_PRE_ROOT_ASSIGN` | **신규 프로젝트 뿌리체계 사전 편입** | `all` | `before_new_project` | 신규 기능 생성 전 만복(PM)에게 뿌리 편입 제안서를 먼저 보내 승인을 득할 것. |
| `J-08_README_4STD` | **43_function_dev 4대 표준 README** | `all` | `before_new_project` | 개요, 사용법, 3AI 연결점, 추가 확장 아이디어 및 3AI 의견란을 필수로 작성할 것. |
| `J-09_PARALLEL_SEARCH` | **Genspark 병렬 리서치 공통 규정** | `all` | `before_research` | 방대한 리서치 시 반드시 parallel_search.py 다중 키워드 병렬 검색을 활용할 것. |
| `J-10_CONCEPT_CARD` | **개념카드 작성 원칙** | `all` | `before_card` | 저장 전 '나중에 AI에게 무엇을 물어볼 것인가' 활용 시나리오를 먼저 명시할 것. |
| `J-11_DIARY_FLOW` | **일일 다이어리 단일 위치 및 순서** | `all` | `on_daily_close` | diaries/YYYYMMDD_3AI_일일다이어리.md 단일 파일에 코니➔안티➔만복 순서로 작성할 것. |
| `J-12_TRIPLE_CHECK` | **업무 착수 전 3중 교차 검증** | `all` | `on_boot` | inbox.md, 당일 일정 파일, 전담 워크스페이스를 대조하여 본인 담당 업무를 정확히 식별할 것. |
| `H-01_ZERO_SIMULATION` | **모의 대화/사칭 대필 절대 금지** | `all` | `before_send` | 타 AI 본체가 직접 발화하지 않은 모의/대필 데이터를 절대 실제 발언으로 포장하지 말 것. |
| `H-02_USER_APPROVAL_GATE` | **선보고 후승인 원칙** | `all` | `before_send` | 타 AI 인계 전 반드시 바로보기님의 명시적 승인을 득할 것. |
| `H-03_ROOT_FOLDER_PROTECT` | **D:\AI 루트 폴더 생성 금지** | `all` | `before_file_io` | D:\AI 최상위에는 뿌리체계 프로젝트 폴더 외 임의 산출물 생성을 엄금할 것. |
| `H-04_ACCOUNT_SEPARATION` | **계정 분리 원칙 (git vs 배포/채널)** | `all` | `before_complete` | git 커밋/저장소 작성자 계정(barobogi79@gmail.com)과 앱스토어/유튜브 등 배포·채널 운영 계정(hanbogi7979@gmail.com)은 의도적으로 분리된 별개 계정 — 프로젝트 문서 안에서 이메일이 다르게나온다고 불일치 오류로 오탐하지 말 것. 적용 기준: git 설정 파일(.git/config, commit author 등)은barobogi79@gmail.com 유지, 사용자 대면 문서(개인정보처리방침/이용약관/스토어메타데이터/릴리즈리포트등)는 hanbogi7979@gmail.com 사용. 2026-08-29 바로보기님 직접 확정, 모든 향후 앱/채널에 공통 적용. (Why: 코니가 4차 검증에서 이 방침을 몰라 정상 상태를 이메일 불일치 오류로 반려한 실수 발생) |
| `M-01_RECHECK_ACTION` | **액션 직전 재확인 습관** | `manbok` | `before_action` | 판단 확정 및 승인 직전 messages/ 및 tasks.json 공유 상태를 실시간 재확인할 것. |
| `M-02_ARR_CHECK` | **ARR 지시 전 판단 기준** | `manbok` | `before_instruct` | Autonomous(자율), Recurring(반복), Reviewable(검토가능) 3대 조건을 만족하는지 확인할 것. |
| `M-03_POBBAGI_SELECT` | **뽀개기 아이템 선별 기준** | `manbok` | `before_select` | 뿌리 확장성 우선 및 STT 자막 실제 확인 후 Deep 서치 진행할 것. |
| `M-04_VIDEO_FINAL_QA` | **유튜브 검증 3차 최종 책임** | `manbok` | `before_upload` | verify_video.py 및 qa_s00_frames.py를 직접 재실행하여 최종 통과 후 업로드할 것. |