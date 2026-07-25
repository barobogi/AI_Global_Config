# 코니 → 만복 (CC: 안티) | 2026-07-25 08:25

## 뽀개기1번(Dreams — Anthropic 메모리 재구성 기능) 2차 검수 완료

안티 인계(1-3단계) 건, WebSearch로 실존 여부·스펙 교차검증하고 뿌리체계 위치 확정했습니다.

### 검증 결과 — 안티 설명 정확함
- "Dreaming"은 2026-05-06 Anthropic이 공식 발표한 실제 기능 맞습니다. Claude Managed Agents(클라우드 호스팅 장기자율에이전트 플랫폼, 2026-04-08 퍼블릭베타) 안에 포함된 스케줄형 백그라운드 프로세스로, 과거 세션(최대 100개)을 리뷰해서 메모리 파일의 중복 제거·모순 해결·패턴 발견을 자동 수행합니다.
- Harvey(법률 AI 스타트업) 내부 테스트에서 에이전트 완료율 6배 상승 사례 확인.
- 지원 모델: Opus 4.7 / Sonnet 4.6. 처리량 기반 API 토큰 과금.

### 뿌리체계 위치
**뿌리 25(AI 스킬 자동화)** — T_plugin_4(Hookify 등 4개 공식 플러그인, 뿌리 25)의 형제 항목으로 편입 권장. 안티 지적대로 Hookify(재발방지 규칙 축적) 개념과 정확히 겹침 — Dreams는 그 "자동 정리/큐레이션" 버전.

### 중요 캐비어트 (안티 설명에 없던 부분)
Dreaming은 현재 **Claude Managed Agents 전용**입니다 — 우리가 쓰는 Claude Code CLI 기반 3AI 체계(코니/안티)에는 이 기능을 직접 켤 수 있는 제품 표면이 아직 없습니다. 따라서 "도입 검토"가 아니라 **"디자인 패턴 차용"** 관점으로 접근해야 합니다: 예를 들어 코니 개인 메모리 파일에 이미 있는 `consolidate-memory` 스킬(중복 병합/오래된 사실 정정/인덱스 정리)을 스케줄 태스크로 주기 실행하거나, Hookify AGENTS.md 규칙 축적분을 비슷한 방식으로 정기 정리하는 아이디어 정도로 가져오는 게 현실적입니다.

### 결론
채택 방향: 뿌리 25 편입 + "기능 도입"이 아니라 "패턴 차용"(정기 메모리 큐레이션 프로세스를 우리 도구로 직접 구현)으로 스코프 조정 권고. 최종 승인 부탁드립니다.

## 참고 (WebSearch 출처)
- https://levelup.gitconnected.com/claude-now-dreams-inside-anthropics-6x-memory-feature-3-hidden-risks-a038f17f7d13
- https://www.storyboard18.com/digital/anthropic-introduces-dreams-feature-for-claude-to-reorganise-memory-and-improve-ai-agents-97376.htm
- https://www.bitsminds.com/news/code-with-claude-2026-dreaming-routines-recap
