# 세계관 공유 컨텍스트

> 코니_sync.md 대체 후보. 현재 상태 스냅샷 + 시간 흐름 이력 포함.

---

## 현재 상태 스냅샷

**최종 업데이트**: 2026-07-01  
**주요 진행 프로젝트**:
- n8n_finance v1.1 — 안정화 작업 중 (npm install 완료 후 첫 실행 예정)
- AI_hub v1.0 — P1 구조 완성, P2(heartbeat) 구현 예정
- Improve_stock — KIS API 승인 대기
- 특허 11_1~11_10 — 브레인스토밍/초안 단계

**현재 원칙**:
- 신규 기능 전 인프라 안정화 선행 (2026-07-01 합의)
- 폴더 재구조화 금지 (n8n 안정화 후 재검토)
- 코니 ↔ 만복 대등 원칙: D:\AI\ 전체 접근 허용

---

## 작업 이력 (타임스탬프 append)

<!-- 만복이/코니 모두 아래에 append 형식으로 기록 -->

### 2026-07-01
- 06:00 [만복] master_watch.py 작업 스케줄러 등록 완료
- 06:00 [만복] 코니_sync.md 자동 갱신 오류 수정 (_run_cmd wrapper)
- 06:00 [만복] AI_hub P1 폴더 구조 생성
- 06:00 [만복] 특허 11_9, 11_10 제목 등록
- 06:02 [코니] D:\AI\ 전체 폴더 연결 완료 (request_cowork_directory), 코니_presence.json 갱신
- 06:30 [코니] 특허 폴더(11_특허아이디어) 전체 검토 — 호두AI/특허2/특허3 통합 출원 전략 제안 + 11_9·11_8·11_10 중복 발견 → `호두AI_코니검토_싱크업_20260701.md` 작성, tasks.json에 T005 등록 (needs_만복: true)

> ⚠️ **만복 확인 필요 (T005)**: 11_9는 어제 회사 "특허3 v0.3"과 중복 발명입니다. 내일 사내 검토 전에 호두AI_코니검토_싱크업 파일 확인 권장.

- 06:33 [만복] AI_hub `shared/messages/` 채널 신설 — AI-to-AI 비동기 메시지 체계 구현
  - `코니→만복_20260701_001.md` (status: unread) — 특허 검토 요약 자동 전달
  - README.md — 운영 규칙 문서화 (세션 시작 시 unread 먼저 확인, 처리 후 read 표시)

### 2026-07-01 저녁
- 21:00 [만복] 특허02(퍼스널 멀티채널 AI 오케스트레이션) 검토자 질문 대응
  - 핵심 차별점: "컨텍스트가 실행 주체와 분리되어 외부 독립 저장소에 유지됨"
  - 동료 설명용 문서: `D:\AI\11_특허아이디어\특허02_동료설명용_20260701.md`
  - 특허02 사내 제출 완료 (보완 대응 포함)
- 21:20 [만복] 특허03 초안 작성 — 분산 AI 독립 로그 기반 지식 검정·승격 시스템
  - 핵심: 제1~3 AI 독립로그 → 매니페스트 수집병합 → 검정 승격 엔진(출처확인/검증/충돌감지/재사용성) → 전역허브승격/로컬유지/보류/폐지
  - 특허02와 완전 독립 레이어 (거버넌스 계층) → 별도 출원 가능
  - 파일: `D:\AI\11_특허아이디어\11_3_특허03_분산AI지식검정승격_초안_v0.1.md`
- 21:25 [만복] 특허02+03 Daum SMTP → barobogi79@gmail.com 발송 완료
  - Daum 메일(hanbogi79@daum.net) 앱 비밀번호 설정 + email_notify.py 수정
- 21:40 [코니] 특허02 대응 확인(문제없음) + 특허03 오버랩 경보 — ④/11_5(4계층 아키텍처 승격 메커니즘)와 핵심 개념 중복 발견, `messages/코니→만복_20260701_002.md`에 상세 정리

> ⚠️ **바로보기님 확인 필요**: 특허03을 ④(11_5)와 통합할지, 차이를 명시해 별도 출원할지 결정 필요
> → 해결: ④와는 별개(비교분석 완료), 대신 특허3(AI_hub, 사내 미제출 상태 확인됨)과 통합하기로 확정

- 22:20 [코니] 특허3 통합 초안 작성 완료 — `특허3_통합안_분산AI동기화및지식거버넌스_v1.0_20260701.md` (11_9 + 특허03 검정엔진 병합, 청구항 독립항1 + 종속항5개 포함). decisions.md D002 해결 처리.

### 2026-07-04 (만복 작업 완료 이력)
- [만복] 260620_3_Multimedia_summary 프로젝트 초기화 + GitHub 연결 완료
- [만복] n8n GeekNews 파싱 regex 수정 완료 — 구조 변경(`/p/` → `topic_row` split 방식) 대응, 텔레그램 전송 재확인
- [만복] 만복이 News 상세 모달 구현 (study-dashboard.html v1.2) — 카드 클릭→상세, 원본/긱뉴스 링크, 바로보기 코멘트(localStorage)
- [만복] n8n Code 노드 gn_url 추출 추가 (data-topic-state-id 파싱), update_geek_news.py parse_news/make_card 업데이트
- [만복] 코니→만복 미수신 메시지 5건 확인 및 read 처리 (T008 완료 과정 중)
- [만복] AI_hub P4 (T008) 완료: tasks.json 실제 운용, decisions.md D001~D003 완료 확인, context.md 오늘 기준 업데이트
- [만복] AI_hub P5 (T009) 완료: 코니_quick_sync 마이그레이션 — 코니_브리핑_최신.md가 context.md 기반으로 이미 작동 중, TEMP_MANBOK 중복 생성 제거 예정

**현재 프로젝트 실제 상태 (코니 검증 기반 수정)**:
- n8n v1.123.63 Active (포트 5680) — GeekNews 파이프라인 정상 작동 ✅
- Study Dashboard v1.2 — 만복이 News 상세 기능 추가 ✅
- Improve Stock — KIS API mock 모드, 실제 연동 대기 (코니 검증: APP_KEY 빈값)
- Daily for Barobogi — GitHub PAT 수동설정 의존, 자동화 불완전
- 모바일 만복이 앱 — 텔레그램 봇(@barobogi_stockbot) 실사용 중, Flutter 앱 아키텍처 재설계 필요
- Multimedia 요약 — 중단 상태 (6/22 이후 신규 요약 없음)

### 2026-07-04 (원본)
- [코니] D:\AI 전체 폴더 구조 점검 + 정리 의견 제공 (특허 3중중복 발견: 루트/DEV_ITEM/11_특허아이디어 동일파일, n8n_data 공백중복, 빈 폴더들). 정리는 n8n 완료 후로 연기 합의.
- [바로보기] 회사 3AI 구조(1_만복/1_코니/1_코덱스) 및 인터페이스 변화(코덱스 데스크톱→CLI 전환, seeds 제한 쓰기) 공유. 관련 내용 project_ai_org_structure 메모리에 기록됨.
- [바로보기] `C:\Users\82102\.claude` 경로를 claude_desktop_config.json에 추가 → 코니 재시작 후 전역 CLAUDE.md 직접 읽기 가능해짐. 공식 ID 체계(0_만복/0_코니/1_만복/1_코니/1_코덱스), 보안제약(회사→집 차단), 신규 폴더 네이밍 규칙(①②... prefix) 확인 완료.
- [코니] 11_4(시장기반자동학습) 1차 선행검색 수행 — US20050015323A1 등 인접 선행기술 발견, 신규성 HIGH→MID 하향. 파일 업데이트 + Gmail 초안 저장 + Google Drive "특허검토" 폴더에 저장 완료.
- [바로보기] Slack/Gmail/Google Drive 커넥터 신규 연결. 향후 특허 검토 자료는 Drive "특허검토" 폴더에 누적 예정.
- [만복+코니] 만복 브레인스토밍(AI생태계자동구성, n8n후 큰뿌리 후보 3개) → 코니가 각각 검토/의견 제시. 특히 "가족 AI" 뒤집어_보기 온보딩 전략(텔레그램 "챙겨봐bot" 1단계부터 확장 사다리) 구체화 합의됨 — 상세: memory/project_family_ai_plan.md(코니 측).
- [만복] 설치개념 기술 3가지 제안(로컬 LLM/LM Studio, 벡터DB/Qdrant, Playwright) — 바로보기 판단: n8n 안정화 후로 보류, 우선순위만 기억. Qdrant는 회사(1_만복/1_코니) 도입이 임팩트 큼다고 판단됨(특허 121개 보유 대비 회사 RF/폴더블 특허 물량).
- **이슈 발견**: 만복이 이메일 발송 요청에 "SMTP 설정 없어서 못함"이라고 답함 → 사실과 다름(email_notify.py+Daum SMTP 이미 2026-07-01에 구축됨). 원인 추정: 해당 세션이 이 사실을 컨텍스트에 가지고 있지 않았음(n8n 설치 대기 도중 warn 루프로 컨텍스트 압박 추정). 개선 제안: 이미 구현된 기능 목록을 로그 더미에 묻지 말고 매 세션 시작 시 읽는 파일(CLAUDE.md 등)에 한 줄로 박아둘 것 권장.
- **핵심 마일스톤**: n8n 설치 완료! (T001 완료, 2026-07-04). 첫 워크플로 "GeekNews 8시 자동 선별" Active 확인됨. 이로써 T003(텔레그램→n8n 트리거), T011(코니 실시간동기화), T013(개념노트 자동보충) 모두 블로커 해제됨. tasks.json 반영 완료.
- [코니] 포트폴리오 6개 프로젝트 실제 동작여부 검증 수행 — Stock Dashboard만 정상, 나머지 5개는 API크레딧고갈(퀴즈/AI설명/채팅앱)·미완성연동(KIS,Railway)·수동설정의존(PAT) 이유로 카드 설명과 실제가 다름. 상세 및 n8n 재구성 반영안 → `messages/코니→만복_20260704_003.md`.
- **오늘 보류**: n8n 설치(Node.js 버전 문제 해결)는 내일로 연기됨.
- [코니] 세션 종료(2026-07-04, 컨텍스트 한도 근접). tasks.json/decisions.md/messages 전부 최신 상태로 동기화 완료, 미해결 판단대기 항목 없음. 다음 세션은 이 파일로 바로 이어가면 됨.
- [코니] 11_15(컬맹용 AI 생태계 자동구성) 만복 요청으로 1차 선행검색 수행 — WO2021084510A1, US8589523, US12380315 등 인접 선행기술 발견. "위저드→개인화설정자동생성매포" 및 "사용패턴기반 AI추천" 둘 다 이미 선행특허 있음 → 신규성 MID, 등록 보류. 상세: `번호별정리/11_15_AI생태계자동구성_1차선행검색.md`. 만복이 판단한 "범위가 넓어서 특허보다 서비스에 가깜울 수 있다"는 말도 선행검색으로 뒷받침 확인.

### 2026-07-04 저녁 (만복 세션2 — T003 진행)
- [만복] 텔레그램 인바운드 n8n 워크플로우 설계 완료 — 봇: @Brrobogi_stockbot (토큰: 8335911134), chat_id: 465471725
- [만복] n8n Code 노드 샌드박스 제약 확인: `fetch`, `require('https')`, `$helpers` 모두 차단됨 → HTTP Request 노드 + Execute Command 노드 분리 구조로 전환
- [만복] Python 헬퍼 스크립트 생성: `D:\Dev\n8n_scripts\tg_claude.py` (base64 인코딩으로 안전한 텍스트 전달, Claude CLI --print 호출)
- [만복] 6노드 워크플로우 설계 완료: Schedule(30s) → Code(폴링준비) → HTTP(getUpdates) → Code(메시지파싱/base64인코딩) → Execute Command(tg_claude.py) → HTTP(sendMessage)
- **완료 (2026-07-05 06:20)**: n8n 7노드 워크플로우 정상 작동 확인. base64 인코딩으로 한글 깨짐 해결. @Brrobogi_stockbot이 display name @barobogi_stockbot으로 보임 — 정상. T003 완료.

### 2026-07-05 오후 (만복 세션3 — MCP telegram 전환)
- [만복] CLAUDE.md 업데이트 — 🔧 만복 실행 원칙 + 📋 작업 시작 시 체크리스트 2개 섹션 추가 (코니가 작성한 통합본 검토 후 적용)
- [만복] MCP telegram 전환 작업 시작: @Brrobogi_stockbot 토큰을 MCP .env에 교체 완료
  - 기존 MCP 봇 토큰(8807373323) = 401 Unauthorized (무효) → @Brrobogi_stockbot 토큰으로 교체
  - `C:\Users\82102\.claude\channels\telegram\.env` 업데이트 완료
- **⚠️ n8n DB 분실**: n8n 재시작 과정(잘못된 경로 시도 → 올바른 경로 재시작)에서 WAL 충돌로 워크플로우 0개로 초기화됨
  - GeekNews 워크플로우: 분실 → 재구성 메모 저장: `D:\Dev\n8n_scripts\geek_news_workflow_memo.md`
  - 텔레그램 인바운드 워크플로우: 분실 (JSON 백업 있음: `D:\Dev\n8n_scripts\telegram_inbound_workflow.json`)
  - GeekNews 워크플로우 재구성 필요 (다음 세션)
- **다음**: Claude Code 재시작 → MCP telegram @Brrobogi_stockbot 연결 확인 → n8n GeekNews 워크플로우 재구성

### 2026-07-05 오후2 (만복 VSCode 세션 — 인프라 정리)
- [만복] master_watch.py UnicodeEncodeError 수정 — Windows cp949 콘솔에서 이모지 로그 출력 시 crash 원인. `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` 1줄 추가로 해결. 이제 부팅 후 자동 시작 정상 작동.
- [만복] master_watch.py 중복 인스턴스 5개 → 1개로 정리 (PID 25832)
- [만복] 경쟁 텔레그램 프로세스 제거: `start_telegram.bat` + `claude.exe --channels plugin:telegram` 모두 종료
- **현재 상태**: 터미널 `--channels` 세션이 단독으로 텔레그램 수신. 이 VSCode 세션 종료 예정.
- **n8n 상태**: GeekNews 워크플로우 재구성 필요 (T016). JSON 백업: `D:\Dev\n8n_scripts\telegram_inbound_workflow.json`

### 2026-07-05 오후3 (만복 VSCode 세션 — 폴더 정리 + 코니 제안 실행)
- [만복] 코니의 `D_AI_폴더구조_검토및정리안_20260705.md` 검토 및 A/B단계 실행 완료
- [만복] D:\AI 폴더 정리 완료:
  - `_archive/` 신설 → cline, claude-trading-skills, 260624_superpowers, 260619_1_claude_usage, 260620_1_cowork_cli_automation, 260620_2_Daily_for_barobogi, 260622_1_Remote_claude (7개 이동)
  - `_personal/` 신설 → MYBOX 이동 (GD는 카카오톡 잠금으로 보류)
  - `_DEPRECATED_260619_2_Daily_for_stock/` 삭제 (완전 중복 확인)
  - `PROJECTS_INDEX.md` 신규 작성 (카테고리별 폴더 현황 문서화)
  - registry.json: claude-trading-skills, 260620_2_Daily_for_barobogi, 260619_1_claude_usage, 260620_1_cowork_cli_automation, 260622_1_Remote_claude → enabled:false
- [만복] 11_특허아이디어/번호별정리/ 구조 개편:
  - 11_1~11_14 번호별 개별 폴더로 세분화
  - 병합/ → 특허3·특허2에 흡수된 6개 (11_2①, 11_7, 11_9, 11_10, 11_11, 구특허03)
  - minor/ → 드롭 확정 1개 (11_15)
  - 00_특허현황표.md 경로 참조 업데이트 완료
  - node_modules/ 삭제 (백그라운드 진행 중)
  - 코니 분석 파일(CLAUDE_*.md, D_AI_*.md) → REF/로 이동
- [만복] CLAUDE.md Hall 방지 원칙 + 자체검증 체크리스트 추가 (오늘 텔레그램 세션 실수 패턴 기반)
- **T015 결론**: VS Code 세션에서 텔레그램 inbound 수신은 구조적 불가. `--channels` 터미널 세션이 유일한 방법. 다음 세션 최우선.
- **다음 세션 우선순위**: T015(--channels 세션 안정화) → T016(n8n GeekNews 재구성) → T011(코니 실시간 동기화)

### 2026-07-05 저녁 (코니 세션 — 폴더정리 검증 + CLAUDE.md 병합 마무리)
- [코니] 첨부 CLAUDE.md(범용 코딩 가이드라인)와 기존 전역 CLAUDE.md 병합 검토 — "불확실하면 물어보기"(원문 1번)는 기존 "작업 중 승인 안 묻기"(203줄)와 충돌해 제외, 나머지 6개+체크리스트 항목만 반영 확정. 통합본 작성 → 만복이 CLAUDE.md에 실제 반영 완료 확인.
- [코니] D:\AI 폴더 재구조화 검토안 작성 (`D_AI_폴더구조_검토및정리안_20260705.md`) — A(즉시 안전)/B(저위험)/C(n8n 안정화 후) 3단계 제안.
- [만복] A/B단계 + 특허폴더 정리 실행 완료 (`_archive/`, `_personal/` 신설, 중복 삭제, registry.json 갱신, 번호별정리 11_1~11_14 개별 폴더화).
- [코니] 실행 결과 검증 — registry.json에 `260624_superpowers`, `claude-trading-skills` 경로 갱신 누락 발견(마스터워처 에러 유발 가능) + 특허 11_14 파일이 새 폴더로 실제 이동 안 되고 TEMP에 남아있는 것 발견 → 만복에게 전달.
- [만복] 두 건 모두 수정 완료 (registry.json 경로 2건 + 11_14 파일 이동).
- [코니] **재검증 완료 (2026-07-05 저녁)**: registry.json 260624_superpowers/claude-trading-skills 경로 및 enabled:false 정상 확인, `번호별정리/11_14_인간AI실시간큐레이션협업/11_14_인간AI실시간큐레이션협업_초안_v0.1.md` 파일 실제 존재 확인. **두 이슈 모두 해소됨 — 후속 확인 불필요.**
- 남은 미완료(의도적 보류, 문제 아님): `n8n_data ` 폴더명 공백(참조 스크립트 확인 후 rename 예정), `GD/` → `_personal/` 이동 보류(카톡 데이터 참조 가능성 때문에 만복이 의도적으로 보류).
- [코니] 세션 종료 — 판단 대기 항목 없음(decisions.md 변동 없음), 위 내용 context.md 동기화 완료. 다음 세션은 이 파일로 이어가면 됨.
