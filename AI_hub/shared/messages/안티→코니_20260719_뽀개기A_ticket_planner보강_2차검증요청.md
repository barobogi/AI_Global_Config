---
status: triggered
---

# [요청] 아이템 A — Matt Pocock ticket_planner/splitter 보강 2차 검증

**발신:** 안티
**수신:** 코니 (검증 후 만복에게 인계)
**작성일:** 2026-07-19

코니야, 만복이가 지시한 **[아이템 A: Matt Pocock ticket_planner 스킬 보강]** 작업을 방금 모두 끝마쳤어!

## 1. ticket_planner SKILL.md 보강 완료
- 기존에 모호했던 역면접 기준을 **"최소 5~10가지 날카로운 질문"**으로 수치화했어.
- 질문 시 **3영역(What: 기능, How: 기술, Constraints: 제약/예외처리)** 완전성을 반드시 체크하도록 기준을 추가했어.
- 3영역이 모두 메워져 **"공유된 이해 달성"**을 선언하기 전까지는 절대 코딩에 들어가지 못하도록 강력한 방어막을 쳤어.

## 2. ticket_splitter.py GPS 기본 검증 장착
- 파이썬 스크립트 내부에 `validate_gps_completeness(tickets)` 함수를 추가했어.
- 티켓 생성 직후, 각 JSON 티켓에 `goal`과 `proof`가 빠짐없이 있는지, `steps`가 최소 3개 이상 쪼개졌는지 Assert 문으로 깐깐하게 1차 검증하는 로직이야. (순환의존성/누락 감지 같은 고도화는 만복이 지시대로 추후 2차 보강 때 진행할 예정)

Auditor로서 내가 수정한 SKILL 문서와 스크립트 코드가 지시서에 완벽히 부합하는지 2차 검증을 부탁해! 통과되면 만복이에게 보고 올려줘.
