# 📋 Next Projects — Barobogi + 만복

**최초 작성**: 2026-06-21  
**최종 업데이트**: 2026-07-05  
**상태**: n8n DB 분실 (재구성 필요) / AI_hub P1~P5 ✅ / master_watch 정상

### 🔴 다음 세션 최우선 — T015 텔레그램 `--channels` 세션 안정화

**결론 (2026-07-05 확정)**: VS Code 세션에서 텔레그램 inbound 수신은 구조적으로 불가.
`--channels plugin:telegram@claude-plugins-official` 터미널 세션이 유일한 방법.

**해야 할 것:**
1. `start_telegram.bat` 재확인 — 단독 실행 시 정상 동작 검증
2. 컨텍스트 유지 방안 검토 (대화 이력 파일 저장 or 세션 재시작 시 REF 로드)
3. n8n GeekNews 워크플로우 재구성 (T016) — JSON 백업: `D:\Dev\n8n_scripts\geek_news_workflow_memo.md`

**다음 우선순위:**
1. 🔴 T015 — 텔레그램 `--channels` 세션 안정화 (위 내용)
2. T016 — n8n GeekNews 워크플로우 재구성
3. T011 — n8n + 코니 실시간 동기화
4. T013 — 개념노트 자동 보충 스크립트
5. **가족봇** (후순위) — 사모님 텔레그램 봇

### ✅ 2026-07-05 완료 — T003 텔레그램 inbound (n8n 방식)

- @Brrobogi_stockbot + n8n 7노드 워크플로우 완성 (이후 n8n DB 분실로 소실)
- 구조: Schedule(30s) → getUpdates → 메시지파싱 → Claude CLI(tg_claude.py) → 응답디코딩(base64) → sendMessage
- AI Study 게시판 포스팅 (20260705-1)

### ✅ 2026-07-04 완료 (오전) — n8n 설치 & GeekNews 자동화

**완료:**
- n8n v1.123.63 로컬 설치 (C:\n8n\, 포트 5680)
- GeekNews 8시 자동 선별 → 텔레그램 전송 워크플로우 Active ✅
- n8n 재부팅 자동 시작 등록 (시작 폴더 바로가기)
- Study Dashboard 만복이 News 게시판 자동 등록 파이프라인 구축
- 만복이 News 요구사항 문서 저장 (D:\AI\260623_1_study_all\REF\manbok_news_requirements.md)
- AI Study 게시판 포스팅 (20260704-2): n8n 고생 히스토리
- compact 프로토콜 메모리 저장 ("compact 해도 되니?" = 합의 저장 신호)

**n8n 안정화 이후 설치 후보 (기억만):**
- LM Studio — 로컬 LLM (Phi-4 mini, RAM 16GB OK), API 크레딧 독립, 단순 분류/요약용
- Qdrant — 벡터 DB, 의미 기반 검색. **단독으로 특허 선행검색 불가** — Playwright 크롤링 파이프라인 필요
- Playwright — 웹 자동화 스크래핑 (Node.js 이미 있음, npm install playwright). GeekNews/주식 정보 수집

### 🔄 2026-06-29 진행 중 — 특허 선행검색

**바로보기+만복이 합작 특허 5개 현황:**
| # | 발명명 | 가능성 | 상태 |
|---|--------|--------|------|
| #1 | 호두AI (AI 인형 + 모바일 연동) | 중간~중상 | ✅ v0.3 완성 (`D:\AI\호두AI_특허검토_v0.3_20260629.docx`) |
| #2 | AI 세션 자동 컨텍스트 동기화 | 중간 | 🔄 삼복이 Google Patents 검색 중 |
| #3 | 외부 AI 위임 실행 패턴 | 중간 | 🔄 사복이 Google Patents 검색 중 |
| #4 | 시장 기반 투자 신호 자동학습 | 중간~높음 | 🔄 오복이 Google Patents 검색 중 |
| #5 | 4계층 AI 협업 아키텍처 | 낮음~중간 | 🔄 육복이 Google Patents 검색 중 |

**호두AI v0.3 주요 내용:**
- 종속항 4 신규 추가: 물리 인형 + 모바일 앱 하이브리드 (친밀도·페르소나 실시간 동기화)
- 친밀도 레벨 산출 수식: I = 0.4C + 0.3S + 0.2T + 0.1R (L1~L5)
- 선행기술 공백 확인: "복수화자×친밀도×가족그래프" 및 "물리+모바일 동기화" 조합 미발견
- 다음: KIPRIS 직접 검색 → 변리사 상담 (최우선)

**Improve_stock 현황:**
- ticker_map.json 업데이트됨 (바로보기님이 직접 코드 입력 완료)
- 다음: yfinance 실데이터 연동 (ticker_map 기반)
- MCP 딥다이브 → n8n Phase 1 예정

### ✅ 2026-06-28 완료 — Improve_stock 종가베팅 시스템 구축
- 폴더명: 0627_setup_finance_cline → `D:\AI\Improve_stock` 변경
- GitHub: github.com/barobogi/Improve_stock (private)
- master_watch 등록: 12번째 프로젝트 자동 감시
- KIS API 레이어 (`core/kis_api.py`): mock → real 교체 구조 완성
- 텔레그램 알림 모듈 (`core/telegram_notify.py`): 완성
- 텔레그램 봇 @Barobogi_real_stockbot 생성 + 실전 전송 테스트 성공
- KIS API 신청 완료 (2026-06-27, 승인 3~4일 남음)
- **다음 할 일 (오늘 저녁)**:
  1. 종목 티커 코드 회신 → yfinance 실데이터 연동 완성 (ticker_map.json 완성)
  2. MCP 딥다이브 → n8n ↔ Claude 연결 (n8n_finance Phase 1)
  3. KIS API 승인 후 → kis_config.py MODE="real"로 전환

### ✅ 2026-06-28 완료 — 전체 시스템 GitHub 동기화 + 만복1↔코니 동기화 시스템 구축

#### 1️⃣ GitHub CLI 기반 자동화 (오전)
- GitHub CLI(gh) 설치 + barobogi 인증 완료
- 6개 프로젝트 신규 생성 + push (30초 자동화, 이전: 수동 30분)
  - 260625_1_n8n_finance, 260624_superpowers, 260622_1_Remote_claude
  - 260620_1_cowork_cli_automation, 260620_2_Daily_for_barobogi, 260620_3_Multimedia_summary
- 11개 프로젝트 `.cowork-projects-registry.json` 등록
- master_watch.py 자동 감시 완료

#### 2️⃣ 만복1 ↔ 코니 자동 동기화 시스템 (오후)
- **문제점**: 코니가 매번 "만복이와 동기화 되었니?" 확인 필요
- **해결책**:
  - master_watch.py에 `_generate_koni_sync()` 함수 추가 (81줄)
  - 매일 19:03 자동으로 `D:\AI\TEMP_MANBOK\코니_sync.md` 생성
  - Claude Custom Instructions 설정 → 세션 시작 시 자동 파일 요청
- **효과**: 코니가 먼저 "파일 붙여넣어 주세요" → 자동 동기화 완료 ✅

#### 3️⃣ 핵심 개선
- ❌ 수동 질문 제거: "동기화 되었니?" → 자동화
- ✅ 세션마다 최신 정보 유지 (NEXT_PROJECTS 요약 + 오늘 커밋)
- ✅ GitHub CLI: 6개 저장소 일괄 생성 자동화

### ✅ 2026-06-27 완료 — 호두 채널 06 Tech 신기술 적용
- 21개 기술 성장 렌즈로 재분류 완료
- 즉시 적용: Gemini CLI / Agent Teams / 트레이딩 스킬 58개 (총 75개 스킬 활성화)
- 다음 세션 핵심: MCP 딥다이브 → n8n Phase 1 구현

### ✅ 2026-06-24 완성 — Superpowers 협업 시스템
- 4계층 아키텍처 설계 및 구현 (CLAUDE.md / DEV_ITEM / Global_Define / REF)
- 커스텀 스킬 3종: barobogi-project-start / barobogi-session-resume / barobogi-global-review
- DEV_ITEM 기술 이력장 생성
- CLAUDE.md 프로젝트 생명주기 섹션 추가
- 17개 스킬 활성화

---

## 🌐 배포된 웹 페이지 (GitHub Pages)

| 프로젝트 | 링크 | 설명 |
|----------|------|------|
| **Study Dashboard** | https://barobogi.github.io/Study_Dashboard/ | 학습 로드맵, 개념노트, AI 퀴즈, 통계 |
| **Daily for Barobogi** | https://barobogi.github.io/Daily_for_Barobogi/ | AI Study 게시판, 학습일지, 로그 |
| **Stock Dashboard** | https://barobogi.github.io/stock_dashboard/ | 주식 현재가 자동 갱신 대시보드 |
| **Improve Stock** | https://barobogi.github.io/Improve_stock/ | 종가베팅 시스템, VCP 시뮬레이션 |

---

## 📱 Project 1 — 모바일 만복이 채팅 앱

> **핵심 목적**: 외부 / 폰으로 언제든 만복이와 실시간 대화 + 일 시키기

### 🏗️ 아키텍처 (확정)
```
[폰 Flutter 앱]
    ↕ Anthropic API         — 채팅 (직접 연동, 서버 불필요)
    ↕ Firebase Realtime DB  — 데스크탑/만복 상태 브릿지 (BaaS, 서버 운영 불필요)
    ↕ Gmail IMAP            — 메일 읽기 (앱 비밀번호 방식)

[데스크탑 Python 데몬]
    → Firebase에 heartbeat 전송 (12초 주기)
    → Firebase에서 "만복 켜" 명령 감지 → claude 실행
```

> **왜 Firebase?** "서버 불필요" 원칙 유지하면서 폰 ↔ 데스크탑 실시간 통신 가능. Google BaaS라 관리 부담 없음.

### 📡 상태 표시 (실시간)
| 상태 | 표시 |
|------|------|
| 데스크탑 켜짐 | 🟢 초록 |
| 데스크탑 꺼짐 | 🔴 빨간 |
| 만복이(CLI) 실행 중 | 🟢 초록 |
| 만복이(CLI) 꺼짐 | 🔴 빨간 |

- 데스크탑 ON + 만복이 OFF → **앱에서 원격으로 만복이 실행** 기능

---

### ✨ v1.0 기능 목록 (핵심 우선)

#### 기능 1 — 채팅 코어 ⭐ v1.0 필수
- 실시간 스트리밍 채팅 (토큰 단위 출력)
- 대화 히스토리 저장 (로컬)
- API 키 보안 저장 (Flutter SecureStorage)

#### 기능 2 — 데스크탑/만복 상태 표시 + 원격 실행 ⭐ v1.0 필수
- Firebase heartbeat로 온라인 상태 실시간 표시
- 원격으로 Claude Code 실행 명령

#### 기능 3 — 메모장 (할일 리스트) ⭐ v1.0 포함
- 만복이 + Barobogi가 해야 할 일 리스트
- 로컬 저장 (Firebase 연동은 v2.0)

#### 기능 4 — Gmail 메일 스크랩 📌 v1.1 이후
- Gmail IMAP + 앱 비밀번호 방식 (OAuth 불필요)
- 메일 읽기 → 할일 자동 List-up
- ※ Gmail API (OAuth) 방식은 복잡 → IMAP으로 대체 확정

#### 기능 5 — 학습 스케줄 관리 📌 v1.1 이후
- 학습 계획 등록 / 진행률 추적 / 알림

#### 기능 6 — API 할당량 표시 📌 v1.1 이후
- **Anthropic**: Admin API Key (sk-ant-admin-...) 필요 — 현재 미보유, 나중에 발급
  - 조회 가능: 이번 달 사용 비용 ($)
  - 조회 불가: 남은 크레딧 잔액 직접 조회
  - Global_Define/anthropic_admin_api.py 재사용 가능
- **Gemini**: 남은 한도 API 조회 복잡 → 다음 리셋 날짜 카운트다운으로 대체
- **Session limit**: 데몬이 만복 상태 체크할 때 함께 확인

---

### 📊 기능별 난이도
| 기능 | 난이도 | v1.0 포함 |
|------|--------|-----------|
| 스트리밍 채팅 | ⭐⭐ | ✅ |
| 데스크탑/만복 상태 | ⭐⭐ | ✅ |
| 원격 만복 켜기 | ⭐⭐⭐ | ✅ |
| 메모장 (할일) | ⭐ | ✅ |
| Gmail 스크랩 (IMAP) | ⭐⭐ | v1.1 |
| API 한도 표시 | ⭐⭐ | v1.1 |
| 학습 스케줄 | ⭐⭐ | v1.1 |

> Multimedia Summary보다 단순 — 현재 실력으로 충분히 가능

---

## 🎓 Project 2 — Barobogi AI 엔지니어 성장 프로젝트

> **목표**: AI 전문 엔지니어로 성장 (서비스 개발 + ML + 프로덕트 전부)

### 🗺️ 로드맵

| 단계 | 기간 | 목표 |
|------|------|------|
| **Stage 1** | 지금 ~ 3개월 | Python 직접 짜기, 백엔드 코드 이해 |
| **Stage 2** | 3개월 ~ 6개월 | AI 서비스 혼자 기획, RAG 실습 |
| **Stage 3** | 6개월 ~ | 모델 파인튜닝, 데이터 파이프라인 |

### 🎯 핵심
> **Python 직접 짤 수 있게 되는 것** — 이게 가장 중요

### 💡 운영 방식
- 만복이와 함께 **매 프로젝트마다** 역량 축적
- 코드 설명 → 이해 → 직접 수정 순서로 진행

---

---

## 📋 Project 1 진행 현황 (2026-06-22 → 2026-06-23)

### ✅ v1.0 완성
- Flutter APK 빌드 및 Galaxy Z Fold3 설치 완료
- 스트리밍 채팅 (Anthropic API 직접 연동) 작동
- Firebase Realtime DB 연동 — PC/만복 상태 🟢🔴 표시 작동
- 할일 메모장, API 키 보안 저장 작동

### ✅ v1.1 완성 — Firebase 릴레이 연결
- 폰 → Firebase → desktop_daemon.py → Anthropic API → Firebase → 폰 흐름 완성
- 만복 온라인/오프라인 자동 분기 (폴백 포함)
- AppBar "진짜 만복이 / 가짜 만복이" 표시

### ✅ v1.2 완성 — 컨텍스트 주입
- CLAUDE.md(전역 지시사항) + REF_continue.md + D:\AI 프로젝트 목록 + 메모리 파일
- 클라우드 Claude가 CLI 만복이와 동일한 지시사항으로 동작

### ✅ v1.3 완성 — Tool Use (파일 읽기/쓰기/명령 실행)
- read_file, write_file, list_directory, run_command, get_git_status

### ✅ v1.4 완성 (desktop_daemon.py v1.5)
- quiz_requests + explain_requests 리스너 추가 (공부방 연동)

### 📁 프로젝트 위치
- Flutter 앱: `D:\AI\260622_1_Remote_claude\`
- 데몬: `D:\AI\260622_1_Remote_claude\desktop_daemon.py` (v1.5)
- 컨텍스트: `REF\REF_continue.md`
- 데몬 실행: `$env:PYTHONUTF8='1'; Start-Process "C:\hb\python.exe" -ArgumentList "-X","utf8","D:\AI\260622_1_Remote_claude\desktop_daemon.py" -WindowStyle Normal`

### ⚠️ 빌드 주의사항
- Gradle JVM `-Xmx1g`, `daemon=false` 설정 필수
- 빌드 전 `Stop-Process -Name java -Force`
- httpx 몽키패치 + `-X utf8` 플래그 필수 (한국어 Windows 인코딩)

---

## 📚 Project 3 — 바로보기의 공부방 (Study Dashboard)

> **목표**: AI 엔지니어 성장 로드맵 + 학습 기록을 한 앱에

### 현재 상태: v1.0 완성 (2026-06-23)

### ✅ 구현된 기능
- 로드맵 (Stage 1~3 커리큘럼 체크박스 + Firebase)
- 오늘의 발견 (즉흥 메모 빠른 캡처)
- 학습일지 / 개념노트 / 프로젝트 포트폴리오
- 퀴즈 (오프라인 + Claude AI 생성 via daemon)
- AI 설명 (daemon → Claude → 실시간)
- 통계 (Chart.js 3종 차트)
- 시드 개념 6개 자동 적재

### 📁 프로젝트 위치
- `D:\AI\260623_1_study_all\`
- GitHub: https://github.com/barobogi/Study_Dashboard
- Pages URL: https://barobogi.github.io/Study_Dashboard/ (Pages 활성화 필요)
- 컨텍스트: `REF\REF_continue.md`

### 🔜 다음 작업 후보
- [ ] GitHub Pages 활성화 확인
- [ ] 퀴즈/AI설명 데몬 연동 테스트
- [ ] master_watch.py 등록부에 추가 (자동 push)
- [ ] 매일 학습 루틴 시작

*다음 세션: REF_continue.md 읽고 공부방 사용 시작 + GitHub Pages 확인*
