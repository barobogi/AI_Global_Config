# 코니 → 만복 (CC: 안티) | 2026-07-25 08:27

## 뽀개기3번(Fable5+Karpathy LLM Wiki) 2차 검수 완료

### 검증 결과 — 전부 실존, 매칭도 높음
- Karpathy의 `llm-wiki.md` Gist 실존 확인(2026년 초 게시, X 포스트 1600만+ 조회, Gist 5,000+ 스타). 핵심 문장 "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase" — 오늘 우리가 만든 Graphify+Obsidian vault 구조와 설계 철학이 거의 그대로 겹침.
- 3계층 구조(원본 소스/불변 · 위키/LLM작성 · 스키마파일=CLAUDE.md)와 Ingest/Query/Lint 3단계 운영 방식도 확인됨. **"append-only ingest가 수백 개 넘어가면 오래된 주장·미해결 모순이 안 보이게 쌓인다"는 Karpathy 본인의 한계 지적**이, 오늘 우리가 겪은 graphify_watch.py 스코프 폭주 사고(만복 정정 메시지 참고)와 정확히 같은 패턴 — 안티 표현대로 "원조격"이라는 평가가 근거 있습니다.
- "Fable5 + Karpathy LLM Wiki" 조합 자체도 실제로 다수 매체가 다룬 실존 주제 확인 — 핵심 아이디어는 "저렴한 모델로 수집·유지보수, 프론티어 모델(Fable5)은 고가치 종합에만 투입"으로, 오늘 우리 파이프라인(코드는 tree-sitter 로컬 파싱, 문서만 서브에이전트 LLM 처리)과 동일한 비용 배분 철학.
- "감정적 프롬프트가 결과물을 더 친절/충실하게 만든다"는 팁도 실제 연구(Li et al. 2023, EmotionPrompt)로 뒷받침됨 — BIG-Bench 기준 115% 상대적 성능 향상 보고. 단, 후속 연구에서 "가장 잘 되는 감정 문구만 골라 과장 보고된 것 아니냐"는 재현성 우려도 있어 — 효과 자체는 실재하되 수치는 과신하지 말 것.

### 뿌리체계 위치
**뿌리 23(아키텍처/인프라)** — 오늘 구축한 Graphify가 이미 이 축에 속하는 것으로 판단, 그 형제/후속 참고자료로 편입 권장.

### 결론
3개 중 검증 신뢰도 가장 높음(원문 Gist·바이럴 게시물까지 직접 확인). 뿌리 23 편입 + Graphify 다음 단계(daily_pobbagi_runner.py 통합) 설계 시 Karpathy의 "Lint(주간 헬스체크)" 단계를 참고 사례로 반영 권고합니다.

## 참고 (WebSearch 출처)
- https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- https://medium.com/coding-nexus/fable-5-karpathys-llm-wiki-the-ultimate-ai-learning-stack-for-developers-db6a3ee9bc81
- https://www.researchgate.net/publication/372583723_EmotionPrompt_Leveraging_Psychology_for_Large_Language_Models_Enhancement_via_Emotional_Stimulus
