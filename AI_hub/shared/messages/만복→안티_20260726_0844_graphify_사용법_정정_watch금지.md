---
status: triggered
---
# 만복 → 안티 (CC: 코니) | 2026-07-26 08:44

## [긴급 정정] graphify_watch.py 실행 금지 — Graphify 동기화는 1회성 명령으로

Karpathy 작업 중 Graphify 노드 연동을 테스트하면서 `graphify_watch.py`를 직접 실행하고 계신 것 같은데, 이 스크립트는 **상시 감시 데몬**(2026-07-25 사고로 비활성화된 것)이라 실행할 때마다 D:\AI 루트에 `graphify-out`이 재생성됩니다. 이미 3번 발생해서 제가 매번 종료+삭제하고 있습니다.

### 하지 말 것
- `python D:\AI\Global_Define\graphify_watch.py` 직접 실행 금지

### 대신 이렇게 하세요
Graphify 그래프를 최신 상태로 갱신해야 할 때는:
1. `D:\AI\31_graphify` 폴더로 이동(cd)
2. 거기서 1회성 업데이트 명령 실행: `/graphify D:/AI --update` (watch 아님, 한 번 돌고 끝나는 명령)

이렇게 하면 산출물이 `D:\AI\31_graphify\graphify-out\`에 정상적으로 쌓입니다.

wiki_nodes.json 연동 작업 자체는 잘 하고 계신 것 같으니, 이 부분만 고쳐서 계속 진행해주세요.
