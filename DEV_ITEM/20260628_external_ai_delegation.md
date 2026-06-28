---
name: external-ai-delegation
description: 비싼 반복 작업을 외부 AI에 위임하고 결과만 Claude로 수집하는 패턴
metadata:
  type: project
---

# 외부 AI 위임 실행 패턴

바로보기님이 고안한 아이디어. /GOAL의 반복 토큰 소모 문제를 해결.

## 핵심 개념
- 만복이 = 설계자 + 판단자 (고비용, 고품질)
- Gemini CLI / 다른 AI = 실행자 (저비용, 반복 가능)
- 파일 시스템 = 결과 전달 매개체

## 패턴
```
만복이: 목표 + 함수 정의 → job.py 생성
n8n:   스케줄로 Gemini CLI 실행 트리거
Gemini: 반복 수행 → results.json 저장
만복이: 다음 세션에 results.json 읽고 판단 + 업데이트
```

## 적용 후보
- 백테스팅 자동화 (매일 전략 검증)
- 동영상 뽀개기 학습카드 품질 검증
- 코드 에러 자가 수정 루프
- 신호 통계 자동 집계

## 인프라 (이미 있음)
- Gemini CLI: 설치 완료
- n8n: 설치 중 (트리거 역할)
- 파일 시스템: results.json 저장소

## Why
/GOAL은 실시간 토큰 소모 → 주기적 실행 시 Max 구독 필요.
외부 AI 위임 시 Claude 토큰 절약 + 무제한 반복 가능.
