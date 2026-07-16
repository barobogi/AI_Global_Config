# 📥 3AI 지식 인박스 (Knowledge Inbox)

내일(또는 다음 뽀개기 세션) 최우선으로 분석 및 구현할 아이템 대기열입니다.

## [1순위 🔥 오늘 당장 착수] LangGraph 기반 AI 에이전트 개발 뽀개기
- **링크**: https://youtu.be/3My9sphTxtk?si=Ymx4kxDRW_mM9vDn
- **채널**: 블루닷 AI
- **주제**: AI 에이전트 개발, 이 영상 하나로 끝냅니다. (LangChain + LangGraph)
- **등록일**: 2026-07-16
- **착수일**: 2026-07-17 (오늘 최우선)
- **목표**:
  - 9시간 분량의 LangGraph 오케스트레이션 기법 완벽 분해.
  - T026(MSA 통신구조) 이후 우리 3AI가 나아갈 Multi-LLM 에이전트 라우팅 설계안 벤치마킹.
  - **특허 11_18(MCP 브릿지 이종 동기화) v0.2 보강용** 기존 기술 대비 차별성 분석.

## [2순위 🔧 롤백 필요] T024 VibeCoding - Claude CLI 원복 작업
- **지시**: 만복 PM 반려 (2026-07-16) → API 직접 호출 → Claude CLI subprocess 방식으로 원복
- **근거**: 전역 원칙 위반 (API 회피 구조 설계가 기본)
- **방향**:
  - `Claude CLI subprocess (--output-format json --print)` 방식으로 전면 롤백
  - 수정 완료 후 코니 검토 → 만복 승인 절차 준수
