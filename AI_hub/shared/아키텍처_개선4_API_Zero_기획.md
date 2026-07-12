# 아키텍처 개선 4 — API Zero 메모리 기획서

작성: 만복 / 2026-07-12  
목표: 외부 API 요금 없는 로컬 지식 파이프라인 구축

---

## 1. 현재 외부 API 의존성 지도

### 🔴 유료 (크레딧/비용 발생)

| 서비스 | 사용처 | 현재 상태 |
|--------|--------|-----------|
| **Anthropic API** | `Multimedia_summary/claude_service.py` (요약 생성) | 실사용 중 (크레딧 필요) |
| **Anthropic API** | `desktop_daemon.py` (공부방 채팅) | 비활성 (크레딧 소진으로 중단) |
| **OpenAI TTS** | T063 유튜브 TTS | 계획 중 (착수 전) |
| **ElevenLabs** | T063 유튜브 TTS 대안 | 계획 중 (착수 전) |

### 🟡 무료 (쿼터/한도 있음)

| 서비스 | 사용처 | 한도 |
|--------|--------|------|
| **YouTube Data API v3** | `youtube_pobbagi.py`, T018 RSS 파이프라인 | 일 10,000 유닛 |
| **Firebase Realtime DB** | `concept_booster.py`, Study Dashboard, T018 결과 저장 | 1GB / 10GB 전송 |
| **Telegram Bot API** | 두복이, 승인봇(T020) | 무료 (속도 제한만) |

### ✅ 이미 API Zero

| 기능 | 이유 |
|------|------|
| `youtube_pobbagi.py` 자막 추출 | LLM 없이 자막 직접 가져옴 |
| `concept_booster.py` | Firebase만 사용, LLM 없음 |
| T018 RSS 파이프라인 | YouTube API + Firebase (LLM 없음) |
| master_watch.py | 자체 로직만 (외부 API 없음) |

---

## 2. 개선 방향 (3단계)

### 1단계 — Anthropic API 크레딧 의존성 제거 (단기, 만복 직접)

**Multimedia_summary 요약 생성:**
- 현재: `claude_service.py` → Anthropic API 크레딧 소비
- 개선: Claude Code CLI subprocess 방식으로 교체
  ```python
  # 변경 전
  client = anthropic.Anthropic(api_key=API_KEY)
  response = client.messages.create(...)
  
  # 변경 후 — 구독 세션 활용 (크레딧 0)
  result = subprocess.run(
      ["claude", "-p", prompt, "--output-format", "json"],
      capture_output=True, text=True
  )
  ```
- 효과: API 크레딧 0원, Claude Code 구독 내에서 해결

**desktop_daemon.py 채팅:**
- 이미 Remote Control 방식으로 대체 계획됨 → 별도 작업 불필요

### 2단계 — Firebase 로컬 대체 (중기, 안티 위임)

**현재 Firebase 사용 목적:**
- 개념노트 저장/조회 (concept_booster.py ↔ Study Dashboard)
- T018 파이프라인 결과 저장

**대체 방안: 로컬 SQLite + GitHub Pages 정적 JSON**
```
[Python 스크립트] → SQLite (로컬) → JSON 익스포트 → GitHub Pages
[Study Dashboard] → GitHub Pages의 JSON 직접 읽기 (Firebase 불필요)
```
- 효과: Firebase 쿼터 제약 없음, 인터넷 없어도 동작, 속도 향상
- 주의: Study Dashboard HTML 수정 필요 (Firebase SDK → fetch JSON)

### 3단계 — YouTube API 캐싱 강화 (중기)

- 동일 채널 재조회 시 로컬 캐시 우선 사용 (이미 일부 구현됨)
- 일 10,000 유닛 → 실제 사용량 모니터링 후 필요 시 적용

---

## 3. 우선순위 결정 (바로보기님 확인 필요)

| 우선순위 | 항목 | 효과 | 난이도 |
|----------|------|------|--------|
| **HIGH** | Multimedia_summary Anthropic API → CLI subprocess | 즉시 비용 0 | 낮음 |
| **MID** | Firebase → 로컬 SQLite + GitHub JSON | 외부 의존성 제거 | 중간 |
| **LOW** | YouTube API 캐싱 강화 | 쿼터 절약 (현재 여유) | 낮음 |
| **보류** | T063 TTS — OpenAI 유지 | 저작권 규칙상 상업 허가 API 필수 | — |

---

## 4. 즉시 착수 가능 항목

**Multimedia_summary claude_service.py 수정** — 만복 직접, 30분 내 완료 가능.

바로보기님 승인 시 바로 진행하겠습니다.

---

## 5. 담당 확정 (바로보기님 결정 대기)

- 1단계: **만복** (claude_service.py 수정)
- 2단계: **안티** (SQLite 파이프라인) / **코니** (Study Dashboard HTML 수정)
- 3단계: 현재 여유 있으면 보류
