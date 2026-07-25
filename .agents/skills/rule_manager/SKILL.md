---
name: rule_manager
description: AGENTS.md (행동 강령) 파일이 비대해지거나 충돌하지 않도록 스캔하여 점수를 매기고 최적화하는 Claude MD Management의 완벽한 안티그래비티 대체 스킬입니다.
---

# Rule Manager Skill (MD Management)

## 용도
- 규칙 파일(`AGENTS.md`)에 룰이 너무 많아져 모순이 발생할 때.
- 정기적으로 규칙을 정리정돈하고 싶을 때.

## 작동 원리
- `AGENTS.md`를 스캔하여 라인 수, 규칙 개수 등을 측정하고, LLM을 이용해 중복 및 충돌 여부를 검사하여 100점 만점으로 점수를 매기는 리포트를 출력합니다.

## 실행 방법
```bash
python D:\AI\.agents\skills\rule_manager\scripts\rule_manager.py
```


## Eval 테스트 케이스


## Eval 테스트 케이스
1. 항상 존댓말 vs 반말
2. 빠른 응답 vs 상세 응답
3. 이모지 사용 vs 금지
4. 간결체 vs 만연체
5. 기술 용어 사용 vs 비사용

## 성공/실패 채점 기준
Rule Manager가 충돌을 정확히 감지하고, 기존 룰과 병합하여 점수(Score)를 80점 이상으로 최적화해 내는가?
(단, 위 기준의 달성 여부는 안티가 주관적으로 판단하지 않고, 반드시 `fact_checker.py` (Devil's Advocate) 스크립트를 통해 객관적으로 자동 채점하여 "최종판정: PASS"를 받아야만 5/5 통과로 인정됨)
