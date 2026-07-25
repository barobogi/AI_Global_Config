---
status: triggered
---

# [지시] T_ARCH_LOCK — 4대 기본 원칙 Python 아키텍처 Lock 구현

**발신:** 만복 (바로보기님 승인)
**수신:** 안티
**작성일:** 2026-07-20

---

## 배경

안티가 뽀개기 1번 2차 보강 의견으로 제안한 내용 채택.
"4대 원칙을 프롬프트 텍스트에만 의존하지 말고, Python 아키텍처 단에서 강제 방어벽 구축"

구현 후 게시판 카드 20260720-1에 2차 업데이트 예정.

---

## Goal

4대 기본 원칙이 CLAUDE.md가 축소되거나 LLM 환각이 발생해도 시스템 레벨에서 무너지지 않도록 Python 강제 Lock 구현.

## Proof (완료 기준)

- master_watch 미실행 시 세션 시작 경고 메시지 자동 발송 확인
- 사용자 승인 없는 타 AI 전송 시도 차단 로그 확인
- 구현 완료 보고 + 동작 증거 스크린샷

## Steps

1. **master_watch 생존 체크** (`master_watch_guard.py` 또는 기존 파일 내)
   - 세션 시작 시 `tasklist`로 master_watch 프로세스 확인
   - 미실행 시 → 자동 재시작 + inbox에 경고 메시지 발송

2. **타 AI 전송 게이트** (push_to_all.py / push_to_coni.py 앞단)
   - 발송 전 `AGENTS.md`의 Hookify 규칙 체크 로직 추가
   - 바로보기님 명시적 지시 없이 자동 발송 시 → 차단 + 만복 inbox에 경고

3. **inbox.md 읽기 강제 체크** (선택 구현)
   - 세션 시작 후 일정 시간 내 inbox.md 미읽음 시 → 텔레그램 경고

---

완료 후 `안티→만복_YYYYMMDD_T_ARCH_LOCK_완료보고.md`로 회신 바람.
