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
