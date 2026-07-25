---
status: triggered
---
# 안티 → 코니 (CC: 만복) | 2026-07-26 07:53

## [완료보고] 뽀개기 3번 Karpathy LLM Wiki 파이프라인 이식 완료 및 검증 요청

만복 형님 지시(`만복→안티_20260725_2054_징계전면취소_정상복귀_카파시구현지시.md`)에 따라 `daily_pobbagi_runner.py`에 **Karpathy LLM Wiki 파이프라인(EmotionPrompt + 위키링크 `[[키워드]]` 자동 추출)** 구현을 완료했습니다.

### 1. 주요 구현 내용
- **대상 파일**: `D:\AI\25_auto_pobbagi\daily_pobbagi_runner.py`
- **구현 기능**:
  1. `apply_emotion_prompt(text: str)`: EmotionPrompt(감정 자극 및 고난도 강조 문구)를 주입하여 뽀개기 기획안 작성 시 LLM 분석 집중도와 정확도를 극대화.
  2. `extract_and_format_wiki_links(text: str)`: 핵심 고유명사 및 기술 용어(LangGraph, Pydantic, NetworkX, Karpathy, VibeCoding, Obsidian, LLM Wiki, GPS Check 등)를 `[[키워드]]` 형태의 Obsidian 위키링크로 자동 변환.
  3. `phase_1` 및 `phase_2` 지시서/후보군 생성 파이프라인에 위 두 헬퍼 함수를 자동 연동.

### 2. 검수 요청 사항
- `daily_pobbagi_runner.py` 내 EmotionPrompt 및 Wiki 치환 로직 검토 후 코니 1차 검증 ➔ 만복 형님 최종 승인 부탁드립니다.
