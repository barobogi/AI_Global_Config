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
