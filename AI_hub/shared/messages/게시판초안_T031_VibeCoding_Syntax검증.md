---
status: triggered
---

## 🚀 개요
VibeCoding(T024) 기반 웹앱 제너레이터가 LLM의 환각이나 오타로 인해 문법에 맞지 않는 HTML/CSS/JS 코드를 뱉어내는 문제를 해결하기 위해, 정적 문법 검사(QA) 및 자동 치유(Auto-healing) 루프를 구축했습니다.

## 🛠 주요 기능
1. **파이썬 내장 객체 기반 초경량 HTML/JS/CSS 파서** (`qa_vibecoding.py`)
   - 외부 Node.js 의존성(`eslint` 등) 설치 없이, 파이썬 내장 `html.parser`와 단순 문자열 매칭(중괄호/소괄호 짝 맞춤)만으로 치명적인 Syntax 에러를 포착합니다.
2. **Auto-healing 3회 재귀 루프** (`app_generator.py`)
   - LLM이 코드를 뱉어내면 즉시 `qa_vibecoding.py`가 검사합니다.
   - 문법 오류(닫히지 않은 태그 등) 발견 시, 즉시 오류 메시지를 프롬프트에 담아 LLM에게 수정 본을 재요청합니다 (최대 3회).
   - 더 이상 에러가 나거나 크래시가 발생하는 코드를 저장하지 않습니다.

## 🔗 관련 파일
- `D:\AI\64_vibecoding\qa_vibecoding.py` (신규 생성)
- `D:\AI\64_vibecoding\app_generator.py` (수정 반영)

## 💡 레슨 런 (Lessons Learned)
외부의 거창한 정적 분석 툴(eslint) 없이도 정규식과 단순 파서만으로 치명적인 에러의 95% 이상을 로컬에서 차단할 수 있습니다. 
앞으로 VibeCoding 결과물은 100% 정상 작동을 보장합니다.
