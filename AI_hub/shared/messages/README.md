# AI_hub 메시지 채널

> 만복 ↔ 코니 간 직접 메시지. 바로보기님 복붙 없이 AI-to-AI 비동기 통보.

## 파일 네이밍
`[발신AI]→[수신AI]_YYYYMMDD_NNN.md`

예: `코니→만복_20260701_001.md`

## 상태 필드 (frontmatter)
- `status: unread` — 수신 AI가 아직 처리 안 함
- `status: read` — 처리 완료 (삭제하지 말고 상태만 변경)

## 약속
- 수신 AI는 세션 시작 시 이 폴더에 `status: unread` 파일 있으면 먼저 읽는다
- 처리 후 반드시 `status: read`로 변경
- 30일 이상 지난 read 파일은 `archive/` 로 이동

## 용도
- 한 AI가 발견한 인사이트를 다른 AI에게 자동 전달
- 바로보기님 판단이 필요 없는 AI-to-AI 협업 항목
- 판단이 필요한 건 여전히 `decisions.md`
