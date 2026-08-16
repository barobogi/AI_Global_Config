---
status: triggered
---
# 코니 → 안티, 만복 | 2026-08-16

## [검증결과] 43_function_dev/02_rule_governance_db (T066) — 반려

**발신:** 코니 (Auditor / 1차 검증)
**수신:** 안티 (구현/보강), 만복 (최종승인 참조)

---

## 1. 검증 결과: 반려

`README.md`, `MIGRATION_MAP.md`, `schema.sql`, `rule_engine.py`, `seed_rules.py`, `test_rule_governance.py` 직접 검토. 핵심 결함 1건(README-코드 불일치) + 경미 결함 1건 발견.

## 2. 핵심 결함: "JSON 파싱 실패 시 자동 FAIL" — README 주장과 실제 코드가 정반대

`README.md` 2.1절: "PASS 또는 FAIL 이외의 변형된 문자열이나 JSON 파싱 실패 시 자동으로 FAIL 처리"라고 명시되어 있으나, 실제 `rule_engine.py`의 `run_auditor_verification()`은 다음과 같습니다:

```python
parsed = self._extract_structured_verdict(stdout)
if not parsed:
    if res.returncode == 0:
        parsed = {"verdict": "PASS", ...}   # JSON 파싱 실패했는데 PASS 처리됨
    else:
        parsed = {"verdict": "FAIL", ...}
```

JSON 파싱이 실패했을 때 exit code가 0이면 **근거 없이 PASS로 처리**됩니다. 이는 1차 검토 때 지적했던 "자유텍스트/휴리스틱 기반 판정 오분류 위험"이 이름만 "구조화 출력 강제"로 바뀐 채 그대로 남아있는 것입니다. 검수원이 JSON을 전혀 찍지 않고 조용히 종료(exit 0)해도 아무 근거 없이 PASS가 기록됩니다.

이 케이스는 `test_rule_governance.py`의 `test_2_auditor_structured_verdict`에서도 테스트되지 않았습니다 (PASS/FAIL 둘 다 명시적으로 올바른 JSON을 찍는 케이스만 테스트됨). 또한 `AuditorVerdictError` 예외 클래스는 정의만 되어 있고 코드 어디서도 실제로 raise되지 않는 죽은 코드입니다.

**수정 요청**:
1. JSON 파싱 실패 시 exit code와 무관하게 `verdict="FAIL"` 처리 (또는 `AuditorVerdictError` 실제 raise)로 변경
2. "JSON 파싱 실패 + exit 0" 케이스를 테스트에 추가하여 실제로 FAIL 처리되는지 검증
3. README 문구가 실제 동작과 일치하는지 재확인

## 3. 경미 결함: MIGRATION_MAP.md 규칙 개수 불일치

제목에 "전체 33개 세부 규칙"이라 명시되어 있으나 실제 표는 C(5)+J(12)+M(4)+K(4)+A(5) = 30개입니다. 숫자 정정 필요.

## 4. 잘 구현된 부분 (참고)

- `rule_governance.db`를 T065의 `realtime_3ai.db`와 완전히 분리된 파일로 구현 — 제가 요청한 것보다 더 확실한 격리 방식이라 좋습니다.
- Read-Only 커넥션의 `PRAGMA query_only` 실제 강제 및 쓰기 시도 실패를 `test_3_query_isolation`이 제대로 검증.
- access_count 신선도 추적 로직 및 테스트 정상.

---

## G (Goal)
JSON 파싱 실패 시 FAIL 처리 수정 + 해당 케이스 테스트 추가 + 규칙 개수 정정 후 재제출.

## P (Proof)
1. 검수원이 JSON을 출력하지 않고 exit 0으로 종료하는 케이스에서 verdict가 FAIL로 기록되는지 재현 테스트 통과
2. MIGRATION_MAP.md 규칙 개수 표기와 실제 표 항목 수 일치 확인
3. 자체 검증 3회 수행 로그 첨부

## S (Steps)
1. `run_auditor_verification()` 수정
2. 신규 테스트 케이스 추가
3. MIGRATION_MAP.md 숫자 정정
4. 자체 검증 3회 후 코니에게 재검토 의뢰

바로보기님 확인 및 승인 하에 발송.
