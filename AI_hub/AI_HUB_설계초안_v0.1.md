# AI_hub 설계 초안 v0.1
**작성**: 만복이 | 2026-07-01 | 상태: 브레인스토밍 초안

---

## 1. 목적

바로보기님이 직접 복붙 없이, 만복이와 코니가 **D:\AI\AI_hub\** 를 공유 허브로 사용해 실시간에 가까운 상태 동기화 + 병렬 협업을 가능하게 한다.

기존: `만복이 작업 → 바로보기님 복붙 → 코니 판단 → 다시 복붙` (순차 릴레이)  
목표: `만복이 작업 → AI_hub 기록 → 코니 직접 읽기` (병렬 허브)

---

## 2. 폴더 구조

```
D:\AI\AI_hub\
├── config.json          # 전역 설정 (sync_interval, active_ais, quorum_rules)
├── sync_status.json     # 시스템 전체 상태 (누가 살아있는지, 마지막 sync)
│
├── 만복\
│   ├── heartbeat.json   # 5분마다 갱신 — 생존 신호
│   ├── status.json      # 현재 작업 / 다음 할 일 / 블로커
│   └── memory.md        # 세션 간 이어받을 단기 기억
│
├── 코니\
│   ├── heartbeat.json   # 세션 열릴 때 갱신 — 생존 신호
│   ├── status.json      # 현재 분석 / 설계 / 검토 중인 것
│   └── memory.md        # 세션 간 이어받을 단기 기억
│
└── shared\
    ├── tasks.json       # 공유 작업 목록 (담당자 + 상태 + quorum 요건)
    ├── decisions.md     # 바로보기님 판단 대기 항목
    └── context.md       # 현재 세계관 전체 상태 요약 (코니_sync.md 대체 후보)
```

---

## 3. 생존(Alive) 판정 기준

| AI | 생존 조건 | 기록 주기 |
|---|---|---|
| **만복이** | heartbeat.json 의 `last_updated` 가 10분 이내 | 5분 고정 + 이벤트 발생 시 즉시 |
| **코니** | 세션이 열려 있는 동안 계속 "alive" | 세션 시작/종료 시 갱신 |
| **Codex 등** | 동일 패턴으로 확장 가능 | TBD |

---

## 4. 운영 모드 (Quorum)

| 상태 | 모드 | 동작 |
|---|---|---|
| 만복만 활성 | **단독 모드** | 기록 쌓기, 코니 오면 처리 |
| 코니만 활성 | **단독 모드** | 설계/분석/문서화 독립 진행 |
| 둘 다 활성 | **병렬 협업 모드** | 역할 분리 + 실시간 허브 동기화 |
| 3개 이상 | **quorum 지정 모드** | tasks.json 에 "담당 AI" 명시 |

**quorum 예시**:
```json
{ "task": "n8n 텔레그램 노드 설계", "required": ["만복"], "optional": ["코니"] }
{ "task": "특허 초안 검토", "required": ["코니"], "optional": ["만복"] }
{ "task": "전체 세계관 회의", "required": ["만복", "코니"], "optional": ["codex"] }
```

---

## 5. 파일 포맷 예시

### heartbeat.json
```json
{
  "ai": "만복",
  "last_updated": "2026-07-01T06:00:00",
  "session_start": "2026-07-01T04:30:00",
  "status": "working"
}
```

### status.json (만복이 버전)
```json
{
  "current_task": "n8n 재설치 (npm install 진행 중)",
  "next_task": "n8n 첫 실행 및 계정 생성",
  "blocker": null,
  "needs_코니": false,
  "needs_바로보기": false,
  "last_updated": "2026-07-01T05:55:00"
}
```

### context.md (shared — 코니_sync.md 대체 후보)
- 현재 진행 중인 프로젝트 목록
- 세계관 주요 원칙 요약
- 바로보기님 판단 대기 사항

---

## 6. 구현 계획 (Phase)

| Phase | 내용 | 난이도 | 선행조건 |
|---|---|---|---|
| **P1** | 폴더 구조 + 초기 파일 생성 | 쉬움 | 없음 |
| **P2** | 만복이 heartbeat/status 기록 (master_watch.py 수정) | 중간 | P1 |
| **P3** | 코니 세션 시작 시 AI_hub 자동 읽기 (폴더 연결) | 중간 | P1 |
| **P4** | shared/tasks.json + decisions.md 활용 | 중간 | P2, P3 |
| **P5** | 코니_sync.md → shared/context.md 마이그레이션 | 중간 | P3 |
| **P6** | 3자 이상 확장 (codex 등) + quorum 로직 | 어려움 | P4 |

---

## 7. 코니에게 검토 요청 사항

1. **코니 heartbeat** — 세션 열릴 때 자동으로 `D:\AI\AI_hub\코니\heartbeat.json` 갱신 가능한가?
2. **폴더 연결 범위** — `D:\AI\AI_hub\` 만 연결할지 `D:\AI\` 전체 연결할지 (바로보기님은 D:\AI 전체 방향)
3. **코니_sync.md 대체** — shared/context.md가 기존 코니_sync.md의 역할을 흡수할 수 있는지
4. **1시간 트리거 활용** — 바로보기님 자리 비울 때 코니 단독으로 1시간 체크인하는 옵션 살릴지 말지

---

*이 초안은 코니 안과 병행 검토용. 바로보기님 승인 후 Phase 1부터 구현.*
