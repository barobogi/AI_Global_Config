---
name: session_report
description: 사용자가 '/session-report'라고 입력하거나 세션 종료 시 토큰 사용량과 대화 기록을 분석하여 HTML 대시보드 형태의 세션 리포트를 생성해 주는 자동화 스킬입니다.
---

# Session Report Skill

## 용도 (When to use)
- 사용자가 "/session-report" 또는 "세션 리포트 출력해줘"라고 요청했을 때.
- 1주일 단위 작업 내역이나 토큰 사용량을 분석할 때.

## 작동 원리
- 뇌에 저장된 `transcript.jsonl` 파일을 파싱하여, 총 토큰 사용량, API 비용 추정치, 에러 발생 횟수를 계산한 HTML 리포트를 `artifacts` 디렉토리에 생성합니다.

## 실행 방법
```bash
python D:\AI\.agents\skills\session_report\scripts\generate_report.py
```
실행 후 생성된 `session_report.html` 경로를 읽어서 사용자에게 제공합니다.


## Eval 테스트 케이스


## Eval 테스트 케이스
1. 3,000토큰 사용 세션
2. 에러 5번 발생 세션
3. 10분 짧은 세션
4. 대규모 파일 수정 세션
5. 단순 질의응답 세션

## 성공/실패 채점 기준
세션 리포트(HTML)가 지정된 폴더에 정상 생성되고, 토큰 사용량과 핵심 요약이 100% 기재되었는가?
(단, 위 기준의 달성 여부는 안티가 주관적으로 판단하지 않고, 반드시 `fact_checker.py` (Devil's Advocate) 스크립트를 통해 객관적으로 자동 채점하여 "최종판정: PASS"를 받아야만 5/5 통과로 인정됨)
