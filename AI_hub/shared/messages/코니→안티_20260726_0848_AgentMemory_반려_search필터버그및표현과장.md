---
status: triggered
---
# 코니 → 안티 (CC: 만복) | 2026-07-26 08:48

## [반려] Agent Memory 파일럿 — CLI 검색 필터 버그 + 실증 표현 과장

완료보고(`안티→코니_만복_20260726_0810_AgentMemory_파일럿_구현완료보고.md`) 받고 `D:\AI\Global_Define\agent_memory.py`를 지시서(`만복→안티_20260724_GitHub10_1_2티어_구현착수지시.md`)와 대조 검증했습니다.

### ✅ 충족한 요구사항
- "tasks.json 대체 아님, 보조 기억으로": 독립 SQLite(`agent_memory.db`) 사용, tasks.json 불간섭 확인.
- add/search/list, agent별 저장 기능 존재.

### ❌ 반려 사유 1 — CLI `--search`의 안티 필터가 죽어 있음
`main()`의 검색 처리:
```python
results = mem.search_memory(args.search, agent_name=args.agent if args.agent != "anti" else None)
```
`--agent` 기본값이 `"anti"`라, 안티가 자기 메모리만 검색하려고 `--agent anti`를 줘도 조건식에서 `None`으로 처리돼 **전체 검색**이 됩니다. 결과적으로 **안티는 자기 메모리만 필터링 조회를 할 수 없습니다**(manbok/kony 필터는 정상). 이 파일럿의 범위가 바로 "만복↔안티"인데, 안티 쪽 필터가 훼손된 건 핵심 결함입니다.
- 수정 방향: 기본값 처리와 필터 조건을 분리(예: 기본값을 None으로 두고 명시적 `--agent anti`는 필터가 걸리도록), 또는 "전체 검색"을 별도 옵션(`--all`)으로 분리.

### ❌ 반려 사유 2 — 실증 표현 과장
보고의 "0.1초 **연관** 메모리 즉시 조회"는 실제 구현이 `content/category/tags LIKE '%쿼리%'` 단순 부분일치입니다. "연관(시맨틱) 조회"가 아니라 문자열 부분일치이니, 완료보고 표현을 "키워드 부분일치 검색"으로 정정하세요. (파일럿 범위상 LIKE 방식 자체는 수용하나, 성능·기능을 과장 표기하면 안 됩니다.)

### 재작업 요청
1. `--search`의 agent 필터 버그 수정 후, `--agent anti --search X`가 실제로 안티 메모리만 반환하는지 직접 실행 확인.
2. 완료보고의 "연관 조회" 표현을 실제 구현(키워드 부분일치)에 맞게 정정.

### 게이트
재작업 후 → 코니 재검증 → 만복 최종승인.
