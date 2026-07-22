# D:\AI 세션 컨텍스트 브릿지 (만복1 → 만복2)

> 세션 시작 시 반드시 이 파일 전체를 읽고 컨텍스트를 복원할 것.

---

<!-- AUTO_STATUS_START -->
## 🔄 최신 상태 (2026-07-21 저녁 종료)

### ✅ 2026-07-21 완료
- **S.02 업로드** — https://youtu.be/jztIKzr453M (46초, 빅데이터 3V)
- **게시판 카드 20260721-1** (T028 홀모지 비즈니스 필터 커스텀)
- **T_ARCH_LOCK 완료** — master_watch_guard + 무단전송 차단 Lock (안티 구현)
- **T028_hormozi_b 완료** — business_filter.py (FEASIBLE 45% / SUSTAINABLE 35%)
- **S.02 길이 기준 확정** — 35~40초 (만복 공식)

### 📋 진행 중 / 내일 할 일

- **코니**: S.03 대본(화 7/22 마감), EP.02 대본(목 7/24 마감), 뽀개기 1~3번 검토(7/22 만복 인계)
- **안티**: S.03 렌더링(목) → T026_eval_pipeline → 인스타 릴스 배포 (T025 Docker Phase1은 위 작업 끝난 뒤 착수 지시 예정, 지금은 과부하라 보류)
- **만복**: S.03 업로드(목)
- **2026-07-26(일)**: EP.02 업로드 + 플러그인 효과 1주일 리뷰

### ✅ 2026-07-22 완료

- 부팅 후 master_watch/kakao_watcher 중복 프로세스 정리 (Startup 바로가기 제거, 태스크 비활성화)
- 뽀개기 3개(만복 담당) 자막 추출 + Deep 서치 + 코니 인계 완료, 안티 담당 2개 GPS 지시서 재발송
- `daily_pobbagi_runner.py`에 GPS 검증(`gps_check.py`) 실제 연결, 메시지 템플릿 GPS 구조화
- T033 tasks.json 상태 오류 수정 (pending → completed)
- 게시판 카드 20260720-3 (RoboNeo 전환) — 안티가 완료, 확인만 함

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
4. **kakao_watcher.py 실행 여부 확인 → 꺼져 있으면 즉시 재시작** (2026-07-22 추가)
   > `C:\hb\python.exe D:\AI\260619_2_Daily_for_stock_TEMP\kakao_watcher.py`
   > Why: 2026-07-22 재부팅 시 Startup 바로가기(KakaoWatcher.lnk)와 Task Scheduler(만복_kakao_watcher)가 동시에 떠서 중복 실행 발견 → 바로가기는 제거하고 만복이 세션 시작마다 직접 확인/기동하는 방식으로 전환
5. 바로보기님께 "동기화 완료 — [핵심 상태 1줄 요약]" 보고

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


## 📋 오늘 만복2 요약 (자동 업데이트)
`D:\AI\TEMP_MANBOK\만복2_오늘정리_20260721.md` — 2026-07-21 19:03 생성
