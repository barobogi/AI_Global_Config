# AI_hub — 만복이 ↔ 코니 공유 허브

**위치**: `D:\AI\AI_hub\`  
**목적**: 바로보기님 복붙 없이 AI 간 상태 동기화 + 병렬 협업  
**버전**: v1.0 (2026-07-01)

---

## 폴더 구조

```
AI_hub\
├── INDEX.md                      ← 이 파일
├── config.json                   ← 전역 설정
├── status\
│   ├── 만복_heartbeat.json       ← 만복이 생존 신호 (5분마다 자동 갱신)
│   ├── 만복_current_task.json    ← 현재 작업 상태 (이벤트 기반 즉시 갱신)
│   └── 코니_presence.json        ← 코니 세션 활성 여부
├── log\
│   └── YYYY-MM-DD.md             ← 일자별 작업 이력
├── memory\
│   ├── 만복\                     ← 만복이 세션 간 기억
│   └── 코니\                     ← 코니 세션 간 기억
└── shared\
    ├── tasks.json                ← 공유 작업 목록 (quorum 기반)
    ├── context.md                ← 세계관 전체 상태 (코니_sync.md 대체 후보)
    └── decisions.md              ← 바로보기님 판단 대기 항목
```

---

## 운영 모드

| 상태 | 모드 |
|---|---|
| 만복 heartbeat 최근 10분 이내 + 코니 세션 활성 | **병렬 협업 모드** |
| 만복만 활성 | **단독 모드** — 기록 누적, 코니 합류 시 catch-up |
| 코니만 활성 | **단독 모드** — 분석/설계 독립 진행 |
| 둘 다 비활성 | **대기** |

---

## 생존 판정 기준

- **만복이**: `만복_heartbeat.json` 의 `last_updated` 가 10분 이내
- **코니**: `코니_presence.json` 의 `session_active: true` 여부

---

## needs_coni 플래그 사용법

`만복_current_task.json` 의 `needs_coni: true` 로 세팅 시:  
→ 코니가 세션 열면 자동으로 감지, 사람 개입 없이 AI끼리 처리  
→ `needs_바로보기: true` 는 사람 판단 필요 → `shared/decisions.md` 에 기록
