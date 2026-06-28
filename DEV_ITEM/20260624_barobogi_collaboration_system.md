---
기술명: barobogi ↔ 만복이 협업 시스템 (4계층 + 3스킬)
작성일: 2026-06-24
적용프로젝트: 260624_superpowers
Global_Define_승격: 미결정
---

## 설명
barobogi(초보 개발자)와 만복이(Claude Code CLI)가 프로젝트를 진행할 때 발생하는 두 가지 구멍(자산 미발견, 세션 품질 불안)을 막기 위한 4계층 아키텍처 + Superpowers 커스텀 스킬 3종 시스템.

## 활용 예상 범위
- 모든 barobogi ↔ 만복이 프로젝트에 공통 적용
- AI 협업 시스템 구축 참고 패턴으로 활용 가능

## 4계층 구조
- Layer 0: CLAUDE.md — 전역 규칙 (모든 프로젝트 자동 적용)
- Layer 1: D:\AI\DEV_ITEM\ — 기술 이력장 (신규 기술 기록)
- Layer 2: D:\AI\Global_Define\ — 기술 창고 (재활용 검증 코드)
- Layer 3: REF\REF_continue.md — 프로젝트 현황

## 핵심 코드 위치
- barobogi-project-start: D:\Dev\superpowers\skills\barobogi-project-start\SKILL.md
- barobogi-session-resume: D:\Dev\superpowers\skills\barobogi-session-resume\SKILL.md
- barobogi-global-review: D:\Dev\superpowers\skills\barobogi-global-review\SKILL.md
- 설계 문서: D:\AI\260624_superpowers\docs\superpowers\specs\2026-06-24-barobogi-manbog-collaboration-system-design.md

## Junction link 배포 패턴
새 커스텀 스킬 추가 시:
1. D:\Dev\superpowers\skills\<스킬명>\SKILL.md 생성
2. New-Item -ItemType Junction -Path "C:\Users\82102\.claude\skills\<스킬명>" -Target "D:\Dev\superpowers\skills\<스킬명>"
3. 즉시 Claude Code에서 사용 가능

## 주의사항
- 배경(background) 서브에이전트에는 권한 승인 불가 → 파일 생성 작업은 foreground 또는 만복이 직접 처리
- CLAUDE.md 추가는 엄격 기준 적용 (모든 프로젝트 해당 + 반복 실수 방지만)
