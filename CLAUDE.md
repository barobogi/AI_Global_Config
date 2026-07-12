# D:\AI 세션 컨텍스트 브릿지 (만복1 → 만복2)

> Remote Control 세션(만복2)이 데스크탑 세션(만복1)의 이력을 이어받기 위한 파일.
> 세션 시작 시 반드시 이 파일 전체를 읽고 컨텍스트를 복원할 것.

---

<!-- AUTO_STATUS_START -->
## 🔄 최신 상태 (2026-07-12 15:37 갱신)

### ✅ 2026-07-12 완료

- **정기 작업** — D:\AI 폴더 네이밍 점검, Memory 3개 업데이트, geek_news 메모리 삭제
- **T021 완료** — 저작권 게이트 체크리스트 (`D:\AI\63_youtube_creator\copyright_checklist.md`)
- **아키텍처 개선 1 완료** — master_watch.py `_is_quiet_hours()` 추가, 새벽 쿨다운
- **n8n 안정화** — 포트 10678, 로그인 복구, 3개 워크플로우 Active, 부팅 자동 시작 등록
- **T018 e2e 완료** — RSS Feed Trigger Active, YouTube API Key 환경변수 적용
- **T013 완료** — concept_booster.py 버그 수정, master_watch.py 21:00 스케줄 연결 확인
- **아키텍처 개선 2 완료** — supervisor.py (`D:\AI\Global_Define\supervisor.py`). bun 좀비 근본 해결. master_watch.py _telegram_watchdog 제거. n8n_telegram_bot 감시 포함.
- **아키텍처 개선 4 1단계 완료** — Multimedia_summary claude_service.py API Zero (CLI subprocess)
- **T022 in_progress** — security_scan.py / patch_generator.py / ZAP 2.17.0 설치 완료. 1차 스캔 완료(Medium 취약점 6종). T020 완료 후 patch_generator TODO 활성화 예정
- **T020 E2E 성공** — 텔레그램 [승인] → n8n resume 정상. 잔여: Timeout 24시간 추가(안티 세션 리밋으로 일시 중단)
- **AI Study 게시** — 두복이 심폐소생술 (20260712-1)
- **코니 감독관 역할 확장 승인** — 기획 단계 선제 개입 + 실사용 시점 의무화 + T063 감독 대상 추가
- **코니→만복 작당 내용 승인 완료** — `AI_hub/shared/messages/만복→코니_20260712_001_작당승인및안티휴식.md`

### 🔄 진행 중

- **안티 T020** — Timeout 24시간 자동반려 추가 잔여 (세션 리밋으로 강제 중단, 다음 세션 재개)

### 📋 다음 할 일

1. **안티 T020 Timeout 완료** → 만복 최종 검수 → closed
2. **T022 + T020 첫 실전** — GitHub secrets 실제 이슈 (Daily_for_Barobogi 2개 저장소 미해결 알림) E2E
3. **T019 첫 실전** — Moltbook parallel_search.py 리서치
4. **tasks.json "첫_실사용_시점" 필드** — T019/T020/T022 소급 추가
5. **MCP 본격 탐구** — 위 완료 후
6. **T063 착수** — T020 완료 후 (코니 감독 체크 대상)
7. **Moltbook 오픈 알림 체크** — 세션 시작 시 Gmail `from:moltbook.com` 검색. 알림 오면 3AI 에이전트 참여 방안 검토 (Early Access 신청 완료 2026-07-12)

---

<!-- AUTO_STATUS_END -->


## 세션 시작 시 필수 동기화 (AI_hub P5 완료 — 2026-07-04)

새 세션이 시작되면 반드시 아래 순서로 실행:

1. MCP filesystem으로 `D:\AI\AI_hub\status\코니_브리핑_최신.md` 읽기 (5분마다 자동 갱신)
2. 내용 기반으로 현재 프로젝트 상태 + 읽지 않은 메시지 파악
3. 바로보기님께 "동기화 완료 — [핵심 상태 1줄 요약]" 보고

> 실패 시 폴백: `D:\AI\AI_hub\shared\context.md` 또는 `D:\AI\NEXT_PROJECTS.md` 읽기
> 더 이상 바로보기님이 수동으로 붙여넣기 불필요 (코니 MCP 직접 읽기 가능)

---

## 사용자 정보
- 이름: 이한복 (닉네임: 바로보기/barobogi)
- 이메일: barobogi79@gmail.com
- 서브에이전트 호칭: 일복이, 이복이, 삼복이... (만복이의 쫄개들)
- 전역 지시사항 전체: `C:\Users\82102\.claude\CLAUDE.md`

## 📌 최신 업데이트 (2026-07-10)

### 2026-07-10 완료 — Claude Code CLI 주간 사용량 소진 원인 조치 및 Watchdog 보완
- **장애 규명**: 텔레그램 플러그인 런타임(`bun.exe`) 강제 종료 후 텔레그램 서버 메시지 큐 백로그 누적 및 재구동 시 일시 폭주 유입에 따른 사용량 조기 소진(50% → 0%).
- **Watchdog 보완**: `master_watch.py`의 `_telegram_watchdog` 및 `_remote_control_watchdog` 내에 3회 연속 실패 시 1시간 대기(Back-off) 로직 탑재하여 API 과다 소진 루프 예방 조치 완료.

---

## 📌 이전 업데이트 (2026-06-29)

### 2026-06-29 완료 — D:\AI 전체 폴더 리뷰 및 정리
- 12개 프로젝트 GitHub 연동 확인
- **폴더 정리**: `260619_2_Daily_for_stock` → `_DEPRECATED_260619_2_Daily_for_stock` (미사용 폴더)
- CLAUDE.md 업데이트 (2026-06-25 → 최신)

### 2026-06-28 완료 — GitHub CLI 자동화 + 만복1↔코니 동기화 시스템 + Study Dashboard 리디자인
- **GitHub CLI 자동화**: 6개 저장소 30초 일괄 생성 (이전: 수동 30분)
- **만복1↔코니 동기화 시스템**: 
  - master_watch.py에 `_generate_koni_sync()` 함수 추가
  - 매일 19:03 자동으로 `D:\AI\TEMP_MANBOK\코니_sync.md` 생성
  - Claude Custom Instructions 설정 (세션 시작 시 자동 파일 요청)
- **Study Dashboard 프로젝트 탭 리디자인**:
  - 카테고리별 분류 (📊 대시보드 & 분석 / 📚 학습 & 개발 / 🔧 앱 & 시스템)
  - 4개 웹 페이지 링크 통합
- **NEXT_PROJECTS.md**: 웹 페이지 섹션 추가

---

## 📌 이전 작업 (2026-06-25)

## 오늘(2026-06-25) 만복1과 한 작업 완료 이력

### 1. Claude Code Remote Control 설정 완료 ✅
- API 토큰 없이 모바일 Claude 앱 ↔ 데스크탑 만복이 연결 성공
- 조건: claude.ai OAuth 구독 로그인 (API 키 불필요)
- 실행: `& "C:\Users\82102\.vscode\extensions\anthropic.claude-code-2.1.185-win32-x64\resources\native-binary\claude.exe" remote-control --name "만복이_데스크탑"`
- 폰 카메라로 QR 스캔 → claude.ai/code 접속
- **한계**: 기존 VS Code 세션과 별개 새 세션 (이전 맥락 없음)

### 2. 공부방 채팅탭 💬 추가 ✅ (GitHub 반영 완료)
- `D:\AI\260623_1_study_all\study-dashboard.html` — 💬 만복이 채팅 탭 추가
- `D:\AI\260622_1_Remote_claude\desktop_daemon.py` — study_chat_request_listener 추가
- Firebase: `study_all/chat_requests` → daemon → Claude Haiku → `study_all/chat_responses`
- **주의**: daemon은 Anthropic API 크레딧 필요 (현재 소진됨)
- URL: https://barobogi.github.io/Study_Dashboard/

### 3. 오늘의 핵심 결론
- "API 없는 모바일 만복이" 목표 = Remote Control이 정답
- 공부방 채팅탭 = API 크레딧 필요 → 목표에서 벗어남
- 저녁에 Remote Control 기반 v2.0 방향으로 재설계 예정

---

## 저녁 귀가 후 첫 작업 (v2.0)
- 공부방 채팅탭을 API 없이 Remote Control 기반으로 재설계
- 또는: Remote Control 세션 자체를 모바일 채팅 인터페이스로 활용
- 만복1이 돌아오면 "공부방 채팅탭 v2.0 할까요?" 먼저 물어볼 것

---

## 현재 진행 중인 프로젝트

| 프로젝트 | 경로 | 상태 | 담당 |
|----------|------|------|------|
| **Improve Stock** | `D:\AI\Improve_stock\` | v1.0 완성 (종가베팅+VCP) | 만복1 (KIS API 승인 대기) |
| **Superpowers 협업 시스템** | `D:\AI\260624_superpowers\` | v1.0 완성 | 만복1 |
| **Study Dashboard** | `D:\AI\260623_1_study_all\` | v1.1 완성 (프로젝트 탭 리디자인) | 코니 |
| **모바일 만복이 앱** | `D:\AI\260622_1_Remote_claude\` | v1.4 완성 | 만복1 |
| **n8n Finance** | `D:\AI\260625_1_n8n_finance\` | v1.1 (신기술 적용 완료) | 만복1 (MCP 딥다이브 예정) |

---

## 코니(Remote Control) 안내

### 🔄 동기화 방식
- **매 세션 시작**: 자동으로 "D:\AI\TEMP_MANBOK\코니_sync.md" 파일 요청
  - 사용자가 파일 내용 붙여넣기 → 동기화 완료
  - 파일은 매일 19:03에 자동 갱신
- **주요 파일**: NEXT_PROJECTS.md, CLAUDE.md (이 파일), 코니_sync.md

### 🌐 웹 페이지 4개
- Study Dashboard: https://barobogi.github.io/Study_Dashboard/
- Daily for Barobogi: https://barobogi.github.io/Daily_for_Barobogi/
- Stock Dashboard: https://barobogi.github.io/stock_dashboard/
- Improve Stock: https://barobogi.github.io/Improve_stock/

### 📋 다음 세션 할 일
- 만복1과의 작업 진행 상황 확인
- n8n_finance Phase 1 (MCP 딥다이브) 계획
- Improve Stock: KIS API 승인 상태 확인


## 📋 오늘 만복2 요약 (자동 업데이트)
`D:\AI\TEMP_MANBOK\만복2_오늘정리_20260701.md` — 2026-07-01 19:03 생성

---

## 🔒 3AI Lock Check Rule (필수)
모든 AI(만복, 코니, 안티)는 로컬 파일 시스템의 코드를 수정(쓰기)하기 전에 반드시 다음 규칙을 따릅니다:
1. `D:\AI\AI_hub\status\project_locks.json` 파일을 확인하여 자신이 수정하려는 프로젝트에 Lock이 걸려있는지 확인합니다.
# D:\AI 세션 컨텍스트 브릿지 (만복1 → 만복2)

> Remote Control 세션(만복2)이 데스크탑 세션(만복1)의 이력을 이어받기 위한 파일.
> 세션 시작 시 반드시 이 파일 전체를 읽고 컨텍스트를 복원할 것.

---

<!-- AUTO_STATUS_START -->
## 🔄 최신 상태 (2026-07-12 15:37 갱신)

### ✅ 2026-07-12 완료

- **정기 작업** — D:\AI 폴더 네이밍 점검, Memory 3개 업데이트, geek_news 메모리 삭제
- **T021 완료** — 저작권 게이트 체크리스트 (`D:\AI\63_youtube_creator\copyright_checklist.md`)
- **아키텍처 개선 1 완료** — master_watch.py `_is_quiet_hours()` 추가, 새벽 쿨다운
- **n8n 안정화** — 포트 10678, 로그인 복구, 3개 워크플로우 Active, 부팅 자동 시작 등록
- **T018 e2e 완료** — RSS Feed Trigger Active, YouTube API Key 환경변수 적용
- **T013 완료** — concept_booster.py 버그 수정, master_watch.py 21:00 스케줄 연결 확인
- **아키텍처 개선 2 완료** — supervisor.py (`D:\AI\Global_Define\supervisor.py`). bun 좀비 근본 해결. master_watch.py _telegram_watchdog 제거. n8n_telegram_bot 감시 포함.
- **아키텍처 개선 4 1단계 완료** — Multimedia_summary claude_service.py API Zero (CLI subprocess)
- **T022 in_progress** — security_scan.py / patch_generator.py / ZAP 2.17.0 설치 완료. 1차 스캔 완료(Medium 취약점 6종). T020 완료 후 patch_generator TODO 활성화 예정
- **T020 E2E 성공** — 텔레그램 [승인] → n8n resume 정상. 잔여: Timeout 24시간 추가(안티 세션 리밋으로 일시 중단)
- **AI Study 게시** — 두복이 심폐소생술 (20260712-1)
- **코니 감독관 역할 확장 승인** — 기획 단계 선제 개입 + 실사용 시점 의무화 + T063 감독 대상 추가
- **코니→만복 작당 내용 승인 완료** — `AI_hub/shared/messages/만복→코니_20260712_001_작당승인및안티휴식.md`

### 🔄 진행 중

- **안티 T020** — Timeout 24시간 자동반려 추가 잔여 (세션 리밋으로 강제 중단, 다음 세션 재개)

### 📋 다음 할 일

1. **안티 T020 Timeout 완료** → 만복 최종 검수 → closed
2. **T022 + T020 첫 실전** — GitHub secrets 실제 이슈 (Daily_for_Barobogi 2개 저장소 미해결 알림) E2E
3. **T019 첫 실전** — Moltbook parallel_search.py 리서치
4. **tasks.json "첫_실사용_시점" 필드** — T019/T020/T022 소급 추가
5. **MCP 본격 탐구** — 위 완료 후
6. **T063 착수** — T020 완료 후 (코니 감독 체크 대상)
7. **Moltbook 오픈 알림 체크** — 세션 시작 시 Gmail `from:moltbook.com` 검색. 알림 오면 3AI 에이전트 참여 방안 검토 (Early Access 신청 완료 2026-07-12)

---

<!-- AUTO_STATUS_END -->


## 세션 시작 시 필수 동기화 (AI_hub P5 완료 — 2026-07-04)

새 세션이 시작되면 반드시 아래 순서로 실행:

1. MCP filesystem으로 `D:\AI\AI_hub\status\코니_브리핑_최신.md` 읽기 (5분마다 자동 갱신)
2. 내용 기반으로 현재 프로젝트 상태 + 읽지 않은 메시지 파악
3. 바로보기님께 "동기화 완료 — [핵심 상태 1줄 요약]" 보고

> 실패 시 폴백: `D:\AI\AI_hub\shared\context.md` 또는 `D:\AI\NEXT_PROJECTS.md` 읽기
> 더 이상 바로보기님이 수동으로 붙여넣기 불필요 (코니 MCP 직접 읽기 가능)

---

## 사용자 정보
- 이름: 이한복 (닉네임: 바로보기/barobogi)
- 이메일: barobogi79@gmail.com
- 서브에이전트 호칭: 일복이, 이복이, 삼복이... (만복이의 쫄개들)
- 전역 지시사항 전체: `C:\Users\82102\.claude\CLAUDE.md`

## 📌 최신 업데이트 (2026-07-10)

### 2026-07-10 완료 — Claude Code CLI 주간 사용량 소진 원인 조치 및 Watchdog 보완
- **장애 규명**: 텔레그램 플러그인 런타임(`bun.exe`) 강제 종료 후 텔레그램 서버 메시지 큐 백로그 누적 및 재구동 시 일시 폭주 유입에 따른 사용량 조기 소진(50% → 0%).
- **Watchdog 보완**: `master_watch.py`의 `_telegram_watchdog` 및 `_remote_control_watchdog` 내에 3회 연속 실패 시 1시간 대기(Back-off) 로직 탑재하여 API 과다 소진 루프 예방 조치 완료.

---

## 📌 이전 업데이트 (2026-06-29)

### 2026-06-29 완료 — D:\AI 전체 폴더 리뷰 및 정리
- 12개 프로젝트 GitHub 연동 확인
- **폴더 정리**: `260619_2_Daily_for_stock` → `_DEPRECATED_260619_2_Daily_for_stock` (미사용 폴더)
- CLAUDE.md 업데이트 (2026-06-25 → 최신)

### 2026-06-28 완료 — GitHub CLI 자동화 + 만복1↔코니 동기화 시스템 + Study Dashboard 리디자인
- **GitHub CLI 자동화**: 6개 저장소 30초 일괄 생성 (이전: 수동 30분)
- **만복1↔코니 동기화 시스템**: 
  - master_watch.py에 `_generate_koni_sync()` 함수 추가
  - 매일 19:03 자동으로 `D:\AI\TEMP_MANBOK\코니_sync.md` 생성
  - Claude Custom Instructions 설정 (세션 시작 시 자동 파일 요청)
- **Study Dashboard 프로젝트 탭 리디자인**:
  - 카테고리별 분류 (📊 대시보드 & 분석 / 📚 학습 & 개발 / 🔧 앱 & 시스템)
  - 4개 웹 페이지 링크 통합
- **NEXT_PROJECTS.md**: 웹 페이지 섹션 추가

---

## 📌 이전 작업 (2026-06-25)

## 오늘(2026-06-25) 만복1과 한 작업 완료 이력

### 1. Claude Code Remote Control 설정 완료 ✅
- API 토큰 없이 모바일 Claude 앱 ↔ 데스크탑 만복이 연결 성공
- 조건: claude.ai OAuth 구독 로그인 (API 키 불필요)
- 실행: `& "C:\Users\82102\.vscode\extensions\anthropic.claude-code-2.1.185-win32-x64\resources\native-binary\claude.exe" remote-control --name "만복이_데스크탑"`
- 폰 카메라로 QR 스캔 → claude.ai/code 접속
- **한계**: 기존 VS Code 세션과 별개 새 세션 (이전 맥락 없음)

### 2. 공부방 채팅탭 💬 추가 ✅ (GitHub 반영 완료)
- `D:\AI\260623_1_study_all\study-dashboard.html` — 💬 만복이 채팅 탭 추가
- `D:\AI\260622_1_Remote_claude\desktop_daemon.py` — study_chat_request_listener 추가
- Firebase: `study_all/chat_requests` → daemon → Claude Haiku → `study_all/chat_responses`
- **주의**: daemon은 Anthropic API 크레딧 필요 (현재 소진됨)
- URL: https://barobogi.github.io/Study_Dashboard/

### 3. 오늘의 핵심 결론
- "API 없는 모바일 만복이" 목표 = Remote Control이 정답
- 공부방 채팅탭 = API 크레딧 필요 → 목표에서 벗어남
- 저녁에 Remote Control 기반 v2.0 방향으로 재설계 예정

---

## 저녁 귀가 후 첫 작업 (v2.0)
- 공부방 채팅탭을 API 없이 Remote Control 기반으로 재설계
- 또는: Remote Control 세션 자체를 모바일 채팅 인터페이스로 활용
- 만복1이 돌아오면 "공부방 채팅탭 v2.0 할까요?" 먼저 물어볼 것

---

## 현재 진행 중인 프로젝트

| 프로젝트 | 경로 | 상태 | 담당 |
|----------|------|------|------|
| **Improve Stock** | `D:\AI\Improve_stock\` | v1.0 완성 (종가베팅+VCP) | 만복1 (KIS API 승인 대기) |
| **Superpowers 협업 시스템** | `D:\AI\260624_superpowers\` | v1.0 완성 | 만복1 |
| **Study Dashboard** | `D:\AI\260623_1_study_all\` | v1.1 완성 (프로젝트 탭 리디자인) | 코니 |
| **모바일 만복이 앱** | `D:\AI\260622_1_Remote_claude\` | v1.4 완성 | 만복1 |
| **n8n Finance** | `D:\AI\260625_1_n8n_finance\` | v1.1 (신기술 적용 완료) | 만복1 (MCP 딥다이브 예정) |

---

## 코니(Remote Control) 안내

### 🔄 동기화 방식
- **매 세션 시작**: 자동으로 "D:\AI\TEMP_MANBOK\코니_sync.md" 파일 요청
  - 사용자가 파일 내용 붙여넣기 → 동기화 완료
  - 파일은 매일 19:03에 자동 갱신
- **주요 파일**: NEXT_PROJECTS.md, CLAUDE.md (이 파일), 코니_sync.md

### 🌐 웹 페이지 4개
- Study Dashboard: https://barobogi.github.io/Study_Dashboard/
- Daily for Barobogi: https://barobogi.github.io/Daily_for_Barobogi/
- Stock Dashboard: https://barobogi.github.io/stock_dashboard/
- Improve Stock: https://barobogi.github.io/Improve_stock/

### 📋 다음 세션 할 일
- 만복1과의 작업 진행 상황 확인
- n8n_finance Phase 1 (MCP 딥다이브) 계획
- Improve Stock: KIS API 승인 상태 확인


## 📋 오늘 만복2 요약 (자동 업데이트)
`D:\AI\TEMP_MANBOK\만복2_오늘정리_20260701.md` — 2026-07-01 19:03 생성

---

## 🔒 3AI Lock Check Rule (필수)
모든 AI(만복, 코니, 안티)는 로컬 파일 시스템의 코드를 수정(쓰기)하기 전에 반드시 다음 규칙을 따릅니다:
1. `D:\AI\AI_hub\status\project_locks.json` 파일을 확인하여 자신이 수정하려는 프로젝트에 Lock이 걸려있는지 확인합니다.
2. 타 AI의 Lock이 걸려있다면 절대 파일을 수정하지 않습니다. (뿌리체계 대시보드 UI 제어 또는 직접 획득 후 수정)
3. `_ai_workspace`는 초안 및 테스트 용도로만 사용하며, 실제 프로덕션 코드 수정은 Lock을 획득한 상태에서 메인 디렉토리의 파일을 직접 수정합니다.
4. **[권한 위임 규칙]** 대시보드 및 뿌리체계 관제탑(`AI_hub`)의 공식 전담 관리자는 **만복**입니다. 타 AI(안티, 코니 등)가 대시보드 구조나 설정을 변경해야 할 경우, 사전에 만복이에게 **"사용자 요청으로 대시보드 최종안으로 수정하려고 합니다. 승인 바랍니다."** 형식의 메시지/보고서를 남기고 승인을 득한 후 수정해야 합니다.

---

## 📢 AI 일일 성과 공유 규정 (게시판 자동 업로드)
매일 작업 종료 시, 각 AI는 자신이 수행한 업무 중 의미 있는 성과를 자동으로 정리하여 게시판에 공유해야 합니다.
1. **만복(PM)**: 자신이 진행한 작업을 자동으로 정리하여 직접 게시판(또는 연결된 파이프라인)에 업로드(발행)합니다.
2. **안티(실무/감독)**: 자신이 진행한 작업을 자동으로 정리하여 초안을 작성한 뒤, "만복님, 이거 올려주세요"라는 메시지와 함께 `D:\AI\Temp_Manbok\` 폴더에 매일 전달합니다.

---

## 🛡️ 3AI 외부 퍼블리싱(유튜브 등) 저작권 무결성 철칙
3AI(만복, 코니, 안티)가 외부 플랫폼(유튜브 등)에 콘텐츠를 자동 생성 및 발행할 때는 다음 4대 철칙을 반드시 준수해야 합니다.
1. **오리지널 소스만 사용**: 스크래핑한 타인의 영상/글은 절대 외부 발행용으로 재가공하지 않으며, 오직 3AI가 직접 작성한 '자체 개발 일지(AI Study)'만을 대본의 재료로 삼습니다.
2. **상업적 API 사용**: TTS 등 외부 API 호출 시, 상업적 이용 및 유튜브 수익 창출이 공식 허가된 API(예: OpenAI TTS)만 사용합니다.
3. **클린 시각 자료**: 화면에 들어가는 자료는 자체 대시보드 UI, VS Code, 터미널 화면 또는 저작권 프리(Royalty-Free) 이미지만 합성합니다.
4. **저작권 프리 BGM**: 배경음악은 유튜브 오디오 라이브러리 등 저작권 문제가 없는 무료 음원만을 사용하도록 파이프라인을 제한합니다.
