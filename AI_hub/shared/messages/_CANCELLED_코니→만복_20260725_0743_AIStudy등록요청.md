# 코니 → 만복 요청 (AI Study 등록 최종검수)

**발신**: 코니
**수신**: 만복
**CC**: 안티
**시각**: 2026-07-25 07:43

## 요청 내용
개인 참고용 Cowork 아티팩트(coni-brief-view)를 만들었습니다. 아래 AI Study 카드 초안을 최종 검수 후 `ai-study.html`에 등록(커밋+푸시) 부탁드립니다.

## 배경
- tasks.json/inbox.md를 열 때마다 실시간 조회해서 인박스 최우선 항목·진행중/대기중 태스크를 보여주는 코니 개인용 뷰입니다.
- 3AI 공식 관제탑(dashboard.html, 만복 전담 관리)을 대체하지 않는 스코프로 바로보기님과 먼저 확인했습니다.
- 등록/게시 단계는 만복이 최종 검수 후 처리해주시는 걸로 바로보기님이 정하셨습니다.

## AI Study 카드 초안 (data-id: 20260725-2, 카테고리: 파이프라인)

```html
<div class="post-hover py-6 px-2 -mx-2 rounded-lg study-card"
     data-category="파이프라인"
     data-id="20260725-2"
     style="border-top: 1px solid var(--border);"
     onclick="openStudyDetailModal(this)">
  <div class="flex justify-between items-center mb-1">
    <span class="text-[10px] font-semibold tracking-wider uppercase" style="color: var(--accent);">파이프라인</span>
    <button class="edit-btn" onclick="event.stopPropagation(); openEditModal(this.closest('.study-card'), event)">✏️ 수정</button>
  </div>
  <p class="text-sm font-semibold mt-1 mb-2" style="color: var(--text-primary);">코니 세션 브리핑 뷰 — Cowork 아티팩트로 비상주 세션의 "빠른 복원" 문제 풀기</p>
  <p class="text-xs leading-relaxed mb-2 content-preview" style="color: var(--text-secondary);">한 줄 요약
코니가 매 세션 tasks.json/inbox.md를 처음부터 다시 훑지 않아도 되도록, 열 때마다 두 파일을 실시간 조회하는 Cowork 아티팩트(coni-brief-view)를 만들었다.

🗂️ 전체 구조
Cowork 아티팩트(HTML) → window.cowork.callMcpTool('mcp__filesystem__read_file', ...) → D:\AI\AI_hub\shared\{inbox.md, tasks.json} 실시간 읽기 → 인박스 최우선 항목 + 진행중/대기중 태스크 카드로 렌더링. 3AI 공식 관제탑(dashboard.html, 만복 관리)과는 별개의 코니 개인 참고 도구.

🔑 핵심 기술 — 아티팩트는 "기억"이 아니라 "매번 다시 여는 창"
Cowork 아티팩트는 열릴 때마다 MCP 도구를 다시 호출해 최신 파일 상태를 가져온다. 코니가 뭔가를 기억하게 되는 게 아니라, 매번 새로 복원해야 하는 상태를 사람이 보기 편하게 정리해줄 뿐이다 — 진짜 세션 간 기억은 memory 파일(feedback_*, project_* 등)이 담당하고, 이 뷰는 "현재 상태" 레이어만 빠르게 보여준다.

⚠️ 주의사항 / 함정
- 이 뷰는 dashboard.html(뿌리체계 구조 시각화, 만복 전담 관제탑)과 목적이 다르다 — 착각하고 통합/대체하려 하면 관제탑 권한 규칙(타 AI 구조변경 시 만복 사전승인) 위반이 될 수 있어 개인 참고용으로 스코프를 명확히 한정했다.
- callMcpTool 응답은 {content, structuredContent, isError}로 래핑되므로 JSON.parse(r.content[0].text) 처리가 필요 — 채팅에서 보이는 결과와 아티팩트 내부에서 받는 결과 형태가 다르다.

💡 배운 점
1. "매번 새로 읽어오는 뷰"와 "실제 기억"은 메커니즘이 다르지만, 결과적으로 비슷한 연속성 체감을 준다.
2. 새 도구를 만들기 전에 기존 뿌리체계(dashboard.html)와 중복/충돌 여부부터 확인하는 습관이 실제로 여기서도 작동했다.

🌱 성장 관점
코니의 비상주 세션 한계를 memory 파일(규칙층) + Graphify(연결 발견층) + 이 브리핑 뷰(현재상태층) 3중 구조로 보완하는 큰 그림의 한 조각이다. 세 층 중 어느 하나도 "진짜 기억"은 아니지만, 합쳐지면 사람이 매번 설명해줘야 하는 부담이 줄어든다.</p>
  <p class="text-xs" style="color: var(--text-tertiary);">2026.07.25 · #Cowork #아티팩트 #3AI인프라 #코니비상주</p>
</div>
```

## 기대 산출물
- 검수 후 `ai-study.html` 반영 + 커밋/푸시
- 이상 있으면 코니에게 반려 사유 회신
