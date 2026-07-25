---
status: triggered
---

# 📋 [보강 지시] 아이템 A — Matt Pocock ticket_planner/splitter 보강

**발신:** 만복 (바로보기님 확정)
**수신:** 안티
**CC:** 코니
**작성일:** 2026-07-19

---

## G (Goal)
ticket_planner 스킬 + ticket_splitter.py에 역면접 기준 명확화 + GPS 기본 검증 로직 추가

## P (Proof)
- ticket_planner SKILL.md에 5~10개 질문 기준 + What/How/Constraints 3영역 명시 확인
- ticket_splitter.py에 validate_gps_completeness() 함수 추가 + 실행 시 검증 통과 확인

## S (Steps)

### 1. ticket_planner SKILL.md 업데이트
역면접 기준 섹션 추가:
- 최소 5~10개 질문 목표
- 3영역 완전성 체크: What(기능) / How(기술) / Constraints(제약)
- 완료 기준: 3영역 모두 커버 시 "공유된 이해 달성" 선언

### 2. ticket_splitter.py에 GPS 기본 검증 추가 (1차만)
아래 함수 추가 후 티켓 생성 직후 호출:

```python
def validate_gps_completeness(tickets):
    for ticket in tickets:
        assert ticket.get('goal'), f"Ticket {ticket['id']}: Goal missing"
        assert ticket.get('proof'), f"Ticket {ticket['id']}: Proof missing"
        assert len(ticket.get('steps', [])) >= 3, f"Ticket {ticket['id']}: Steps < 3"
    return True
```

> ⚠️ 순환의존성/누락 감지는 2차로. 지금은 기본 완전성 체크만.

### 3. 코니에게 2차 검증 요청 (수정 완료 후)

---

완료 후 만복에게 보고.
