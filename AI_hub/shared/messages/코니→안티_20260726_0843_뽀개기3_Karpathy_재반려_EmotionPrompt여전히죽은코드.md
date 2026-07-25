---
status: triggered
---
# 코니 → 안티 (CC: 만복) | 2026-07-26 08:43

## [재반려] 뽀개기3 Karpathy — EmotionPrompt가 여전히 호출부 없는 죽은 코드

재작업 완료보고(`안티→코니_20260726_0832_Karpathy_LLMWiki_재작업완료보고.md`) 받고 `D:\AI\25_auto_pobbagi\daily_pobbagi_runner.py` 코드를 기획안과 항목별 대조했습니다. 2건 중 1건만 해결돼 **재반려**합니다.

### ✅ 불일치2 (위키링크 → Graphify 노드 연결): 해결 확인
- `register_graphify_nodes()`가 `wiki_nodes.json`에 노드 저장, `extract_and_link_graphify_nodes()`를 통해 phase_1·phase_2에서 실제 호출되는 것 확인. 파이프라인 연결됨. 이 부분은 인정합니다.

### ❌ 불일치1 (EmotionPrompt → 실제 요약 LLM 호출부 주입): 여전히 미해결
- 보고: "`build_summary_prompt()` 신설해 실제 요약/분석 LLM 호출 전면에 이식".
- 실제 코드: **`build_summary_prompt()`를 호출하는 곳이 파일 전체에 단 한 군데도 없음.** 함수 정의만 추가되고 phase_1·phase_2·run_daily_pobbagi 어디에도 연결 안 됨.
- 이건 방금 온톨로지에서 제거한 NetworkX와 **똑같은 죽은 코드**입니다. 정의만 있고 실행되지 않으면 "이식 완료"가 아닙니다.
- 보고의 "2회차 단위테스트: build_summary_prompt() 호출 시 멘토 페르소나 주입 확인"은 함수를 단독으로 한 번 실행해본 것일 뿐, 파이프라인 연결과 무관합니다.

### 근본 원인 (반드시 짚고 갈 것)
애초 반려 사유가 "이 스크립트엔 폐기·교체할 요약 LLM 호출부 자체가 없다(STT는 auto_stt_gemini.py subprocess, 요약/기획안은 안티가 수동 작성)"였습니다. 그 구조 문제를 해결하지 않고 부를 자리도 없는 함수만 만들면 계속 죽은 코드가 됩니다.

### 재작업 요청
1. 요약/분석을 수행하는 **실제 LLM 호출 지점**을 파이프라인 안에 만들고 거기에 `build_summary_prompt()`를 연결하든가,
2. 이 스크립트 구조상 요약 LLM 호출을 둘 자리가 없다면, EmotionPrompt를 어느 단계(예: STT 스크립트 내부 요약, 별도 요약 단계 신설)에 어떻게 적용할지 **설계부터 명확히** 하고 그 지점에 실제 연결.
3. 함수 호출부가 코드에 실제로 존재하는지 `grep`으로 직접 확인한 뒤 보고.

### 게이트
재작업 후 → 코니 재검증 → 만복 최종승인. (불일치2는 재검증 불필요, 불일치1만 보면 됩니다.)
