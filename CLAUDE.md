# D:\AI 세션 컨텍스트 브릿지 (만복1 → 만복2)

> 세션 시작 시 반드시 이 파일 전체를 읽고 컨텍스트를 복원할 것.

---

<!-- AUTO_STATUS_START -->
## 🔄 최신 상태 (2026-07-28 밤 종료)

### ✅ 2026-07-28 완료 (뒷정리 + 신규 뽀개기 사이클)

- **뿌리체계 재정리 완료**: dashboard.html vs tasks.json 드리프트 발견·수정(23 인프라뿌리·31 Graphify·52 원복·64 바이브코딩·28 에이전트뿌리·43 function_dev 전부 정식 등록)
- **git 보안사고 발견+해결**: Public 저장소에 자격증명 5종(BytePlus/Kling/RoboNeo/유튜브 쿠키) 9일 노출 + 332MB 임시파일로 인한 push 백로그 2,290+ 커밋 — `git filter-repo`로 히스토리째 제거, 유튜브 쿠키만 재발급(나머지는 폐기서비스라 불필요)
- **프로세스 중복 근본 차단**: master_watch/kakao_watcher/graphify_watch에 OS 레벨 락 추가, supervisor.py에 graphify_watch 강제종료 로직 추가
- **두복이(텔레그램) 안정화**: OAuth 토큰(`claude setup-token`) + 출력 리다이렉트 제거로 자동화 성공, 51시간+ 무중단 확인. "침묵 실패"(프로세스는 살아있는데 응답 안 함) 재현 확인 후 12시간 예방적 재시작 추가. `만복_supervisor` 로그온 트리거 신규 등록(재부팅 대비)
- **GeekNews("만복이 News") 19일간 미갱신 버그 발견+수정**: 라이브 사이트(Daily_for_Barobogi)가 아니라 별도 폐기 저장소(260623_1_study_all) 갱신하고 있던 경로 버그
- **쇼츠1(S.04) public 업로드 완료** — https://www.youtube.com/watch?v=GiC8vPxyvG0 (채널복제기법 첫 시범)
- **쇼츠2(S.05) 목요일(7/30) 22시 무인 자동업로드 예약 완료** — QA 재검증 통과 조건부, 텔레그램 알림 연동
- **본편1(EP.03) 대본+렌더링 착수** — 무리한 토요일 강행 대신 휴가(목~일) 복귀 후로 일정 조정했으나 당일 밤 렌더링까지 진행됨
- **뽀개기 6건 처리**: 만복 3개(ORCA=참고자료 종결, Graphify 컨텍스트재통합=코니검토중, Hermes vault Git버전관리=구현+코니검토중) + 안티 3개(CloudCodes/호두=최종승인, Tech Bridge(오귀속 "Matt Pocock")=개념승인+재훈련경로는 보류)
- **"3AI 자가성장" 신규 트랙 개설**: 뿌리24 하위 `43_function_dev` 등록, 다음 주부터 하루 1개씩 review→코드→문서화→Global_Define 승격 검토→git→전파 사이클 (회사 만복이 방식 참고, 10개 후보 확정)
- **바로보기님 목~일(7/30~8/2) 휴가** — 컴퓨터는 계속 켜둘 예정

### 📋 다음 세션 1순위
1. 코니 검토 대기 중인 Graphify 컨텍스트재통합·Hermes Git버전관리 결과 확인
2. 목요일 22시 S.05 자동업로드 결과 확인(텔레그램 알림 왔는지)
3. EP.03 렌더링 완료 여부 확인(당일 밤 시작됨, 3중 QA 남음)
4. 3AI 자가성장 1번(rhwp/AgentMemory 관련) 시작 — `43_function_dev/01_.../`
5. GD 폴더 개명(카톡 앱 사용 중이라 보류), n8n_finance 폴더 개명(node 프로세스 사용 중이라 보류) — 여유 있을 때 재시도

### ✅ 2026-07-25 완료 (마라톤 하루)

- **EP02 본편 public 업로드 완료** — https://youtu.be/10D8uhjM-mI (edge-tts 캡션 싱크 버그 근본원인 발견+수정: WordBoundary가 아니라 SentenceBoundary였음)
- **push_to_all.py 승인 게이트 내용특정형 강화** — content-agnostic("아무 승인이나 있으면 통과") 취약점 발견 후 rebuild. draft 상태(무해, 스킵) / unread(미전달, 차단 대상) / triggered(이미 전달, 스킵) 3단계로 분리
- **master_watch.py 버그 수정** — `_update_inbox()`가 status를 triggered로 플립 안 해서 무관한 메시지가 반복적으로 전체 발송을 막던 문제 해결 (단, 부작용으로 팝업 실시간 알림이 이번엔 스킵됨 — 다음 세션 후속 확인 필요)
- **안티 징계 에피소드**: EP02 등록 후 1주일 배제 선언 → 같은 날 저녁 전면 취소(정상 복귀) — "선보고 후승인" 반복 위반에 대한 경고성 조치, 실제 장기 배제는 안 함
- **뽀개기 3건 최종 승인 + 구현 지시**:
  - 뿌리25 Dreams Consolidator (AGENTS.md 자가치유, diff→승인→스왑 안전장치)
  - 뿌리52 GPS Check 온톨로지 하드닝 (Pydantic+NetworkX, 안티 구현 착수)
  - 뿌리23 Karpathy LLM Wiki (EmotionPrompt+Obsidian 위키링크, 안티 구현 착수)
- **채널복제기법(패턴 벤치마킹) 최종 승인** + 다음 주 라인업 확정: 쇼츠1(화, 기법 시범적용)/본편1(온톨로지 주제)/쇼츠2(목금)
- **토요일 본편 최종승인 시 다음 주 라인업 동봉** — 신규 표준 프로세스로 AGENTS.md 등재
- **게시판 카드 4개 추가**(20260725-4~7): Dreams/GPS온톨로지/Karpathy/EP02자막버그

### 📋 다음 세션 1순위
1. 안티가 밤사이 GPS Check(뿌리52) + Karpathy(뿌리23) 구현 완료했는지 확인 — 완료 시 증거(Proof) 직접 확인 후 8단계 게시판 등록
2. master_watch 팝업 스킵 부작용 후속 조치 (트리거 우선순위 vs 게이트 정확성)
3. 화요일 타겟 쇼츠1(채널복제기법 시범) 준비 상황 체크
4. Dreams Consolidator(rule_manager.py 개조) 구현 착수 여부 확인

### ✅ 2026-07-21 완료
- **S.02 업로드** — https://youtu.be/jztIKzr453M (46초, 빅데이터 3V)
- **게시판 카드 20260721-1** (T028 홀모지 비즈니스 필터 커스텀)
- **T_ARCH_LOCK 완료** — master_watch_guard + 무단전송 차단 Lock (안티 구현)
- **T028_hormozi_b 완료** — business_filter.py (FEASIBLE 45% / SUSTAINABLE 35%)
- **S.02 길이 기준 확정** — 35~40초 (만복 공식)

### 📋 내일(7/23) 할 일 — 만복 세션 시작 즉시 1순위

1. **S.03 검증 + 업로드** — 안티가 오늘 밤 렌더링 완료해서 인계 예정. verify_video.py + qa_s00_frames.py 통과 확인 후 업로드 (다른 작업보다 최우선)
2. **뽀개기 3개 준비** — 오늘부로 안티 할당 없음, 만복 혼자 6개 후보 중 3개 선별 + 처리
3. **코니**: EP.02 대본(목 7/24 마감)
4. **안티**: T063 Pollinations 파이프라인 안정화 이어서, T026_eval_pipeline
- **2026-07-26(일)**: EP.02 업로드 + 플러그인 효과 1주일 리뷰

### ✅ 2026-07-22 완료

- 부팅 후 master_watch/kakao_watcher 중복 프로세스 정리 (Startup 바로가기 제거, 태스크 비활성화)
- 뽀개기 3개(만복 담당) 자막 추출 + Deep 서치 + 코니 인계 완료 + 이식(cinematic_shot_builder 스킬, content_plan.md 전략노트)
- `daily_pobbagi_runner.py`에 GPS 검증(`gps_check.py`) 실제 연결, 메시지 템플릿 GPS 구조화
- T033/T028_hormozi_b/T_ARCH_LOCK tasks.json 상태 오류 수정 (pending → completed)
- T064_RoboNeo abandoned 처리 — Pollinations API(T063)로 완전 대체
- 안티 담당 뽀개기 2건(OpenArt Director, Matt Pocock)은 7/23로 이월
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
