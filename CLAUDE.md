# D:\AI 세션 컨텍스트 브릿지 (만복1 → 만복2)

> 세션 시작 시 반드시 이 파일 전체를 읽고 컨텍스트를 복원할 것.

---

<!-- AUTO_STATUS_START -->
## 🔄 최신 상태 (2026-07-19 저녁 종료)

### ✅ 2026-07-19 완료
- **EP.01 본편 업로드** ✅ — https://www.youtube.com/watch?v=9Y-PSemx3gM
- **뽀개기 6개 완료** — 게시판 카드 20260719-1~6 등록
- **AGENTS.md 3가지 규정 편입** — 자판기우선법칙 / UglyMVP / 심미안(Taste)
- **뽀개기 자동화 v2** — 반자동 큐레이션, 18:00 자동 가동
- **다음 주 콘텐츠 확정** — S.02(빅데이터3V/화) + S.03(parallel_search/목) + EP.02(좀비프로세스/토)
- **content_plan.md 신설** — `D:\AI\63_youtube_creator\content_plan.md`

### 📋 진행 중 / 다음 할 일

- **코니**: S.02 대본(월), S.03 대본(화), EP.02 대본(목)
- **안티**: 바이브코딩 확장 ③ 인스타 릴스 배포 / Matt Pocock GPS 검증 보강
- **2026-07-26(일)**: 플러그인 효과 1주일 리뷰

<!-- AUTO_STATUS_END -->

---

## 📔 일일 다이어리 규정

- **저장 위치 (단일 고정)**: `D:\AI\AI_hub\shared\diaries\YYYYMMDD_3AI_일일다이어리.md`
- **작성 순서**: 코니 → 안티 → 만복 (통합 총평)
- **트리거**: 매일 20:30 master_watch가 자동 요청 / 바로보기님 종료 선언 후에만 시작
- 세션 시작 시 어제 다이어리 위 경로에서 확인

---

## 세션 시작 필수 동기화

새 세션이 시작되면 반드시 아래 순서로 실행:

1. **`D:\AI\AI_hub\status\inbox.md` 읽기** — 3AI 통합 수신함
2. **`D:\AI\AI_hub\status\telegram_messages.md` 읽기** — 텔레그램 백업
3. **master_watch.py 실행 여부 확인 → 꺼져 있으면 즉시 재시작** (2026-07-20 추가)
   > Why: 종료 루틴이 master_watch를 Stop-Process함 → 재시작 안 하면 18:00 등 예약 자동화 전체 누락
4. 바로보기님께 "동기화 완료 — [핵심 상태 1줄 요약]" 보고

> 폴백: `D:\AI\AI_hub\status\코니_브리핑_최신.md` → `D:\AI\NEXT_PROJECTS.md`
> **⚠️ inbox.md 읽지 않고 "수신함 확인했습니다" 보고 금지 — 부분 확인 = Hall**

---

## 사용자 정보
- 이름: 이한복 (닉네임: 바로보기/barobogi)
- 이메일: barobogi79@gmail.com
- 서브에이전트 호칭: 일복이, 이복이, 삼복이... (만복이의 쫄개들)
- 전역 지시사항: `C:\Users\82102\.claude\CLAUDE.md`

---

## 🔒 3AI Lock Check Rule

파일 수정 전 `D:\AI\AI_hub\status\project_locks.json` 확인 필수.

- 타 AI Lock 걸려 있으면 수정 금지
- `_ai_workspace` = 초안/테스트 전용
- **AI_hub 전담 관리자 = 만복** (타 AI 변경 시 만복 승인 필수)

---

## 📢 AI 일일 성과 공유

- **만복**: 직접 게시판 업로드
- **안티**: 초안 작성 → `D:\AI\Temp_Manbok\`에 전달

---

## 🛡️ 외부 퍼블리싱 저작권 철칙

1. **오리지널 소스만** — 타인 영상/글 재가공 금지, 3AI 자체 작성물만
2. **상업적 TTS** — 구글 클라우드 TTS (Wavenet) 고정
3. **클린 시각 자료** — 자체 UI / Royalty-Free / AI 생성만
4. **저작권 프리 BGM** — 유튜브 오디오 라이브러리만
