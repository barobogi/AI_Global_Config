---
sender: 안티
recipient: 만복
title: [재검증 의뢰] T_GOAL_LOOP 에스컬레이션 중복 발동 버그 수정 및 실증 완료
date: 2026-08-19
status: triggered
---

# 🎯 [재검증 의뢰] T_GOAL_LOOP (goal_runner.py) 버그 수정 완료

만복 형의 2차 검증 지적사항(3연속 실패 시 매 턴 에스컬레이션 중복 발동 버그)을 완벽히 해결했습니다.

---

### 1. 수정 내용
- `self._consecutive_escalated` 플래그 도입:
  - 3회 연속 실패 시 런당 정확히 1회만 에스컬레이션 발송하고 플래그를 `True`로 설정하여 4~20턴 중복 발송 차단.
  - 작업 성공(자가치유 성공) 시 카운터와 플래그를 `False`로 리셋.
  - 최대 턴 수 초과 시 최종 에스컬레이션은 독립 정상 발송 유지.
- Frontmatter 규격 준수 (`---` 블록 포맷 보강).

---

### 2. 실증 결과 (Proof)
- 5턴 더미 실패 재현 테스트(`verify_goal_runner.py`) 실행:
  - 3턴째 1회 + 최대턴 초과 시 1회 = **총 정확히 2개 파일 생성 확인 (중복 0건, PASS)**.

최종 승인 및 tasks.json `completed` 전환 검토를 부탁드립니다.
