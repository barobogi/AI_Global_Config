# D:\AI 프로젝트 종합 감사 리포트

**작성일**: 2026-08-30  
**작성자**: AI Auditor (Cline)  
**범위**: D:\AI 루트 디렉토리 하위 모든 프로젝트  
**목적**: 프로젝트 구조, 코드 품질, 보안, 문서화, 운영 현황 점검 및 개선 제안

---

## 📋 목차

1. [전체 현황 요약](#전체-현황-요약)
2. [프로젝트별 상세 감사](#프로젝트별-상세-감사)
3. [공통 이슈 및 개선 제안](#공통-이슈-및-개선-제안)
4. [우선순위별 액션 플랜](#우선순위별-액션-플랜)
5. [보안 점검 결과](#보안-점검-결과)

---

## 📊 전체 현황 요약

| 구분 | 프로젝트 수 | 비고 |
|------|-------------|------|
| **활성 프로젝트** | 7개 | 25_auto_pobbagi, 63_youtube_creator, 11_특허아이디어, AI_hub, 64_vibecoding, 65_android_apps, 43_function_dev |
| **단일 파일 프로젝트** | 3개 | 26_eval_pipeline, 71_밀리이북, 31_graphify |
| **휴면/아카이브** | 10개+ | _archive, 2606xx 시리즈, DEV_ITEM 등 |
| **인프라/시스템** | 4개 | Global_Define, Antigravity IDE, .claude, .kilo |

**총 코드 라인 수(추정)**: ~15,000+ lines (Python/JS/MD 합계)  
**주 언어**: Python (자동화/파이프라인), Markdown (문서화), JavaScript/TypeScript (웹/앱)

---

## 🔍 프로젝트별 상세 감사

### 1. 25_auto_pobbagi — 유튜브 뽀개기 100% 자동화 파이프라인

#### 📁 구조
```
25_auto_pobbagi/
├── auto_pobbagi_orchestrator.py    # 메인 오케스트레이터 (112줄)
├── auto_pobbagi.py                 # 레거시 단일 파일
├── auto_stt_gemini.py              # STT 추출 (Gemini)
├── youtube_transcript_extractor*.py # Playwright 기반 자막 추출 (2종)
├── youtube_rss_watcher.py          # RSS 감시
├── channel_manager.py              # 채널 관리
├── fact_checker.py                 # 팩트 체크
├── daily_pobbagi_runner.py         # 일일 실행 러너
├── config.json / channels.json     # 설정 파일
├── cookies.txt / drive_token.pickle # 인증 토큰 (⚠️ 보안)
├── transcripts/                    # 출력 디렉토리
└── *.bak 파일들                    # 백업 파일 다수
```

#### ✅ 강점
- 3단계 파이프라인(감지→분석→리뷰) 구조 명확
- 안티/만복 역할 분담 로직 구현
- Playwright로 봇 탐지 우회 구현
- 에러 핸들링 및 재시도 로직 존재

#### ⚠️ 이슈 및 개선점

| 구분 | 이슈 | 심각도 | 제안 |
|------|------|--------|------|
| **보안** | `cookies.txt`, `drive_token.pickle`, `config.json`에 실제 인증 정보 하드코딩 | 🔴 Critical | `.gitignore` 확인, 환경변수/시크릿 매니저로 이관 |
| **코드 중복** | `youtube_transcript_extractor.py` vs `youtube_transcript_extractor_playwright.py` 기능 중복 | 🟡 Medium | 단일 진입점으로 통합, 전략 패턴 적용 |
| **백업 파일** | `*.bak` 파일 6개 루트에 방치 | 🟢 Low | `_backup/` 폴더로 이동 또는 정리 |
| **설정 관리** | 하드코딩된 경로(`D:\AI\25_auto_pobbagi`, `D:\AI\Global_Define\parallel_search.py`) | 🟡 Medium | 설정 파일/환경변수로 외부화 |
| **테스트 부재** | 단위 테스트/통합 테스트 없음 | 🟡 Medium | `pytest` 기반 테스트 추가 |
| **로깅** | `print()` 기반 로깅, 구조화된 로깅 부재 | 🟡 Medium | `logging` 모듈 도입, 로그 레벨 분리 |
| **타입 힌트** | 타입 힌트 미사용 | 🟢 Low | 타입 힌트 추가로 유지보수성 향상 |

---

### 2. 63_youtube_creator — 3AI 연구소 유튜브 채널

#### 📁 구조
```
63_youtube_creator/
├── README.md                    # R&R, 착수 조건, 저작권 철칙
├── content_plan.md              # 콘텐츠 계획
├── copyright_checklist.md       # 저작권 체크리스트
├── pipeline/                    # 파이프라인 (비어있음?)
├── scripts/                     # 스크립트 (비어있음?)
├── _archive/                    # 아카이브
└── 미디어 파일들                # kling_*.mp4, temp_audio.mp3
```

#### ✅ 강점
- R&R(역할 분담) 명확히 문서화
- 저작권 4대 철칙 수립
- 착수 선행 조건 명시로 무리한 착수 방지

#### ⚠️ 이슈 및 개선점

| 구분 | 이슈 | 심각도 | 제안 |
|------|------|--------|------|
| **구현 부재** | `pipeline/`, `scripts/` 디렉토리 비어있음 (착수 대기) | 🟡 Medium | 착수 조건(T011, T018) 완료 시 즉시 구현 착수 |
| **문서 동기화** | `NEXT_PROJECTS.md`의 T063과 연동 확인 필요 | 🟢 Low | 태스크 트래킹 시스템과 연동 |
| **미디어 관리** | 대용량 미디어 파일이 Git에 커밋될 위험 | 🟡 Medium | `.gitignore`에 `*.mp4`, `*.mp3` 추가 확인 |

---

### 3. 11_특허아이디어 — 특허 아이디어 관리

#### 📁 구조
```
11_특허아이디어/
├── PROCESS.md                   # 프로세스 문서 (93줄)
├── 20260629_*.md               # 아이디어 초안들
├── 번호별정리/                  # 코니 정리 파일들
├── 변호별정리/                  # 변리사용 정리
├── minor/                       # 마이너 아이디어
├── REF/                         # 참고 자료
├── TEMP/                        # 임시 파일
└── node_modules/                # ⚠️ 불필요 (Git 제외 확인 필요)
```

#### ✅ 강점
- PROCESS.md로 프로세스 표준화 (6단계 플로우)
- 역할 분담(R&R) 명확
- 선행검색 쿼리 템플릿 제공
- 상태 추적 테이블 관리

#### ⚠️ 이슈 및 개선점

| 구분 | 이슈 | 심각도 | 제안 |
|------|------|--------|------|
| **node_modules** | 루트에 `node_modules/` 존재 (Git 추적 여부 확인) | 🟡 Medium | `.gitignore` 확인, 필요시 제거 |
| **파일 명명** | 날짜 접두사 불일치(`20260629_` vs `20260630_`) | 🟢 Low | 네이밍 컨벤션 통일 |
| **아카이브** | `TEMP/`, `minor/` 폴더 방치 | 🟢 Low | 정기 정리 정책 수립 |
| **자동화 부재** | 선행검색, 상태 업데이트 수동 | 🟡 Medium | 자동화 스크립트 고려 (KIPRIS API 등) |

---

### 4. AI_hub — 3AI 협업 허브

#### 📁 구조
```
AI_hub/
├── AI_HUB_설계초안_v0.1.md      # 설계 문서 (121줄)
├── mcp_server.py                # MCP 서버 구현
├── dashboard.html / dashboard_horizontal.html # 대시보드
├── anti_watchdog.py             # 워치독
├── config.json                  # 설정
├── 만복/ 코니/                  # AI별 워크스페이스
├── shared/                      # 공유 리소스 (tasks.json, decisions.md 등)
├── log/ memory/ messages/       # 로그/메모리/메시지
├── n8n_workflows/               # n8n 워크플로우
└── improvements/                # 개선 사항
```

#### ✅ 강점
- 3AI 협업을 위한 허브 아키텍처 설계
- Heartbeat 기반 생존 판정 시스템
- Quorum 기반 의사결정 모드 정의
- MCP 서버로 도구 확장성 확보
- 대시보드로 가시성 제공

#### ⚠️ 이슈 및 개선점

| 구분 | 이슈 | 심각도 | 제안 |
|------|------|--------|------|
| **설계 미구현** | `AI_HUB_설계초안_v0.1.md`가 v0.1 머물러 있음 (Phase 1~6 중 P1만 완료 추정) | 🟡 Medium | Phase 2~4 우선 구현 (heartbeat 자동화, 코니 연동) |
| **MCP 서버** | `mcp_server.py` 단일 파일, 에러 로그 다수(`mcp_server_*.log`) | 🟡 Medium | 안정성 검증, 구조화된 로깅, 헬스체크 엔드포인트 추가 |
| **대시보드** | HTML 단일 파일, 실시간 업데이트 미지원 (폴링/웹소켓 없음) | 🟡 Medium | WebSocket 또는 SSE 도입으로 실시간성 확보 |
| **파일 기반 동기화** | JSON 파일 기반 동기화 → 동시성 이슈 가능성 | 🟡 Medium | 파일 락(`filelock`) 또는 SQLite WAL 모드 도입 |
| **보안** | `config.json`에 민감 정보 포함 가능성 | 🔴 Critical | 시크릿 분리, 환경변수 사용 |
| **테스트** | 자동화 테스트 부재 | 🟡 Medium | 통합 테스트 시나리오 작성 |

---

### 5. 64_vibecoding — 바이브 코딩 앱 생성기

#### 📁 구조
```
64_vibecoding/
├── app_generator.py             # 메인 생성기 (174줄)
├── qa_vibecoding.py             # QA 검증 모듈
├── generator_trigger.py         # 트리거
├── port_manager.py / port_mapping.json # 포트 관리
├── apps/                        # 생성된 앱들
└── __pycache__/
```

#### ✅ 강점
- Claude CLI 연동으로 LLM 기반 코드 생성
- 화이트리스트 피드백 시스템 (색상/레이아웃/폰트)
- **자가 치유 루프**: QA 에러 시 자동 재시도 (최대 3회)
- **에스컬레이션**: 3회 실패 시 AI_hub 통해 코니/만복 알림
- 포트 관리 시스템으로 충돌 방지

#### ⚠️ 이슈 및 개선점

| 구분 | 이슈 | 심각도 | 제안 |
|------|------|--------|------|
| **하드코딩 경로** | `C:\Users\82102\.vscode\extensions\...` 사용자별 경로 하드코딩 | 🔴 Critical | 설정 파일/환경변수로 외부화, 다중 사용자 지원 |
| **Claude CLI 의존** | `claude.exe` 경로 탐색 로직이 취약 (glob + sorted[-1]) | 🟡 Medium | `which`/`where` 명령 또는 설정으로 경로 지정 |
| **에러 처리** | `subprocess.run` 타임아웃 120초 고정, 인코딩 이슈 가능성 | 🟡 Medium | 설정 가능하게, 에러 분류 세분화 |
| **QA 모듈** | `qa_vibecoding.py` 내용 미확인 (별도 검토 필요) | 🟡 Medium | QA 규칙 문서화, 커스텀 룰 추가 인터페이스 |
| **보안** | 생성된 앱에 민감 정보 포함 가능성 | 🟡 Medium | 생성 전/후 시크릿 스캔 로직 추가 |
| **테스트** | 단위 테스트 부재 | 🟢 Low | 주요 함수별 테스트 케이스 작성 |

---

### 6. 65_android_apps — 안드로이드 앱 아이디어 (공공데이터 API)

#### 📁 구조
```
65_android_apps/
├── API_REGISTRY.md              # API 활용신청 현황 (19줄)
├── PUBLIC_DATA_STRATEGY.md      # 전략 문서
├── .env                         # ⚠️ API 키 저장 (보안)
├── Idea/                        # 아이디어 폴더
└── today_what_to_do/            # 1탄 앱 (구현됨)
```

#### ✅ 강점
- API_REGISTRY로 활용신청 상태 중앙 관리
- 6개 API 모두 승인 완료 (계정키 공유 확인)
- PUBLIC_DATA_STRATEGY로 전략 문서화

#### ⚠️ 이슈 및 개선점

| 구분 | 이슈 | 심각도 | 제안 |
|------|------|--------|------|
| **보안** | `.env`에 실제 API 키/비밀번호 저장, Git 추적 위험 | 🔴 Critical | `.gitignore` 필수 확인, 시크릿 매니저 도입 |
| **문서 동기화** | `today_what_to_do/docs/api/` 하위 문서들과 레지스트리 동기화 수동 | 🟡 Medium | 자동 동기화 스크립트 또는 CI 연동 |
| **아키텍처 문서** | 앱별 아키텍처/코드 구조 문서 부재 | 🟢 Low | 각 앱 폴더에 README.md 표준 템플릿 적용 |

---

### 7. 43_function_dev — 자가성장 아이디어 구현소

#### 📁 구조
```
43_function_dev/
├── README.md                    # 프로세스, 템플릿, 레지스트리 (52줄)
├── _counter.txt                 # 프로젝트 카운터
├── 01_realtime_3ai/             # SQLite WAL + DuckDB 스냅샷
├── 02_rule_governance_db/       # JIT 규칙 인젝터
├── 03_verification_framework/   # 검증 프레임워크
└── 04_public_data_catalog/      # 공공데이터 카탈로그
```

#### ✅ 강점
- 명확한 5단계 사이클 (리뷰→구현→문서화→승격→전파)
- **4대 표준 문서 템플릿** 의무화로 문서 품질 보장
- 카운터 기반 명명 규칙으로 충돌 방지
- Git 커밋 프리픽스 규칙으로 추적성 확보
- DB 스냅샷 정책으로 실시간 DB 보호

#### ⚠️ 이슈 및 개선점

| 구분 | 이슈 | 심각도 | 제안 |
|------|------|--------|------|
| **프로젝트 상태** | 01번만 "승인", 02번 "검증 대기", 03/04번 상태 불명 | 🟡 Medium | 레지스트리 상태 실시간 동기화 자동화 |
| **승격 프로세스** | `Global_Define/` 승격 기준/절차 문서화 부족 | 🟢 Low | 승격 체크리스트 및 자동화 검토 |
| **회사 전파** | "자기완결적 문서" 원칙 좋으나 실제 검증 프로세스 부재 | 🟢 Low | 문서 품질 게이트(린트/링크 체크) 추가 |

---

### 8. 26_eval_pipeline — 스킬 평가 파이프라인

#### 📁 구조
```
26_eval_pipeline/
└── eval_pipeline.py             # 단일 파일 (119줄)
```

#### ✅ 강점
- Gemini API로 스킬 문서 자동 평가
- 테스트 케이스 존재 여부, 정량적 채점 기준 검증
- 시뮬레이션 기반 PASS/FAIL 판정
- 리포트 자동 생성 + AI_hub inbox 연동

#### ⚠️ 이슈 및 개선점

| 구분 | 이슈 | 심각도 | 제안 |
|------|------|--------|------|
| **단일 파일** | 모든 로직이 한 파일에 집중 (SRP 위반) | 🟡 Medium | 모듈 분리: evaluator, reporter, notifier |
| **하드코딩 경로** | `D:\AI\.agents\skills`, `D:\AI\AI_hub\shared\eval_logs` 등 | 🔴 Critical | 설정 파일/환경변수로 외부화 |
| **API 키** | `GEMINI_API_KEY` 환경변수 의존 (관리 방안 문서화 필요) | 🟡 Medium | 시크릿 관리 가이드 문서화 |
| **에러 처리** | API 호출 실패 시 ERROR 판정만 하고 계속 진행 | 🟡 Medium | 재시도 로직, 부분 실패 처리 개선 |
| **테스트** | 자기 자신 평가 불가 (부트스트랩 문제) | 🟢 Low | 메타 평가 스크립트 별도 작성 |

---

### 9. 71_밀리이북 — 밀리/예스24 자동화

#### 📁 구조
```
71_밀리이북/
├── config.json                  # ⚠️ 계정 정보 평문 저장
└── .gitignore
```

#### ⚠️ 이슈 및 개선점

| 구분 | 이슈 | 심각도 | 제안 |
|------|------|--------|------|
| **보안** | `config.json`에 이메일/비밀번호/챗아이디 평문 저장 | 🔴 **Critical** | 즉시 `.gitignore` 확인, 환경변수/키체인 이관, 비밀번호 로테이션 |
| **기능 부재** | 실제 자동화 코드 없음 (설정만 존재) | 🟡 Medium | 구현 계획 수립 또는 아카이브 처리 |

---

### 10. 루트 레벨 파일들

#### 주요 파일 현황
| 파일 | 용도 | 이슈 |
|------|------|------|
| `CLAUDE.md` | 전역 지시사항 | 최신 상태 유지 확인 필요 |
| `PROJECTS_INDEX.md` | 프로젝트 인덱스 | 2026-07-05 이후 업데이트 안됨 (2개월+) |
| `NEXT_PROJECTS.md` | 다음 작업 계획 | 2026-07-19 이후 업데이트 안됨 |
| `package.json` | Node.js 의존성 | `cline` 폴더용, 루트와 무관 |
| `make_patent_docx.py` | 특허 문서 생성 | 단일 목적 스크립트 |
| `merge_patent.py` | 특허 병합 | 단일 목적 스크립트 |
| `youtube_subtitle_extractor.js` | 자막 추출 (JS) | Python 버전과 중복 가능성 |

#### ⚠️ 공통 이슈
- **문서 최신성**: `PROJECTS_INDEX.md`, `NEXT_PROJECTS.md` 2개월 미갱신
- **스크립트 산재**: 루트에 단일 목적 스크립트 다수 → `scripts/` 폴더로 통합 고려
- **임시 파일**: `temp*.txt`, `transcript.txt`, `*.vtt` 등 정리 필요

---

## 🔧 공통 이슈 및 개선 제안

### 1. 설정 관리 통합 (Critical)
```
현재: 각 프로젝트별 config.json, .env, 하드코딩 경로 산재
목표: 중앙 설정 관리 시스템 도입
```
- **제안**: `Global_Define/config.yaml` (또는 TOML) 하나로 통합
- 환경별 설정(dev/prod) 분리
- 시크릿은 별도 `.secrets.yaml` (Git 제외) 또는 OS 키체인/시크릿 매니저

### 2. 로깅 표준화 (High)
```
현재: print(), 파일 로그 혼재, 구조화 안됨
목표: structlog 또는 logging + JSON 포맷 통일
```
- 로그 레벨: DEBUG/INFO/WARNING/ERROR/CRITICAL
- 상관관계 ID(correlation_id)로 요청 추적
- 로그 로테이션/보관 정책 수립

### 3. 테스트 인프라 구축 (High)
```
현재: 거의 모든 프로젝트 테스트 부재
목표: pytest 기반 단위/통합 테스트 + CI
```
- 공통 `conftest.py`로 픽스처 공유
- 커버리지 목표: 70% 이상
- GitHub Actions 또는 로컬 pre-commit 훅

### 4. 타입 힌트 및 정적 분석 (Medium)
```
현재: 타입 힌트 미사용
목표: Python 3.10+ 타입 힌트 전면 적용 + mypy/pyright
```
- 점진적 도입: 신규 코드부터 필수, 기존 코드 순차 적용
- `pyproject.toml`로 도구 설정 통합

### 5. 문서화 표준화 (Medium)
```
현재: 프로젝트별 README 포맷 제각각
목표: 43_function_dev의 4대 표준 템플릿 전 프로젝트 적용
```
- 필수 섹션: 개요, 사용법, 시스템 연계, 확장 아이디어/의견
- Mermaid 다이어그램으로 아키텍처 시각화
- 자동 문서 생성 도구(Sphinx/MkDocs) 검토

### 6. 보안 강화 (Critical)
```
현재: 인증 정보 평문 저장 다수, .gitignore 불완전
목표: 제로 트러스트 시크릿 관리
```
- 즉시 조치: `71_밀리이북/config.json`, `25_auto_pobbagi/cookies.txt`, `65_android_apps/.env`
- `git-secrets` 또는 `truffleHog`로 히스토리 스캔
- 시크릿 로테이션 계획 수립

### 7. 아카이브/정리 정책 (Low)
```
현재: _archive, TEMP, *.bak, node_modules 방치
목표: 정기 정리 자동화
```
- 월 1회 정리 스크립트 실행
- 90일 미수정 임시 파일 자동 아카이브
- `node_modules`, `__pycache__`, `*.pyc` Git 제외 강제

---

## 🛡️ 보안 점검 결과

| 프로젝트 | 민감 파일 | 위험도 | 조치 상태 |
|----------|-----------|--------|-----------|
| **71_밀리이북** | `config.json` (계정/비번) | 🔴 **Critical** | 즉시 조치 필요 |
| **25_auto_pobbagi** | `cookies.txt`, `drive_token.pickle`, `config.json` | 🔴 **Critical** | 즉시 조치 필요 |
| **65_android_apps** | `.env` (API 키) | 🔴 **Critical** | 즉시 조치 필요 |
| **AI_hub** | `config.json` (내용 확인 필요) | 🟡 Medium | 내용 검토 후 조치 |
| **64_vibecoding** | 생성 앱 내 시크릿 가능성 | 🟡 Medium | 스캔 로직 추가 |
| **루트** | `.secrets.json` (존재 확인됨) | 🟡 Medium | 용도 확인 및 관리 |

### 즉시 조치 체크리스트
- [ ] `71_밀리이북/config.json` → 환경변수 이관 후 파일 삭제
- [ ] `25_auto_pobbagi/cookies.txt`, `drive_token.pickle` → 시크릿 매니저 이관
- [ ] `65_android_apps/.env` → `.gitignore` 확인, 시크릿 로테이션
- [ ] `git log --all --full-history -- .secrets.json` 등으로 히스토리 스캔
- [ ] 모든 `.gitignore`에 `*.env`, `config.json`, `cookies.txt`, `*.pickle` 패턴 추가 확인

---

## 📋 우선순위별 액션 플랜

### 🔴 P0 - 즉시 (이번 주)
1. **보안 취약점 패치**: 위 3개 프로젝트 시크릿 즉시 이관 및 로테이션
2. **Git 히스토리 스캔**: 과거 커밋에 유출된 시크릿 확인 및 BFG Repo-Cleaner 등으로 정리
3. **`.gitignore` 전수 조사**: 모든 프로젝트 필수 제외 패턴 적용 확인

### 🟠 P1 - 1주일 내
4. **설정 관리 통합**: `Global_Define/config.yaml` 설계 및 마이그레이션 시작
5. **로깅 표준화**: 공통 로깅 모듈(`Global_Define/logging_utils.py`) 작성 및 25_auto_pobbagi 적용
6. **문서 최신화**: `PROJECTS_INDEX.md`, `NEXT_PROJECTS.md` 현재 상태 반영

### 🟡 P2 - 2주일 내
7. **테스트 인프라**: `pytest` 설정, 26_eval_pipeline부터 단위 테스트 작성 시작
8. **타입 힌트 도입**: `pyproject.toml` 설정, 43_function_dev 프로젝트부터 적용
9. **AI_hub Phase 2~3 구현**: heartbeat 자동화, 코니 세션 연동

### 🟢 P3 - 1개월 내
10. **문서 템플릿 전파**: 43_function_dev 표준을 전 프로젝트 README에 적용
11. **CI/CD 파이프라인**: GitHub Actions로 린트/테스트/빌드 자동화
12. **모니터링/알림**: AI_hub 대시보드 실시간화, 실패 알림 텔레그램 연동
13. **아카이브 정리**: `_archive`, `TEMP`, `*.bak` 일괄 정리 스크립트 작성 및 실행

---

## 📈 메트릭스 및 KPI 제안

| 지표 | 현재 | 목표 (3개월) | 측정 방법 |
|------|------|--------------|-----------|
| **보안 이슈 수** | 3 Critical | 0 | 트러플호그 스캔 주간 실행 |
| **테스트 커버리지** | ~0% | 70%+ | pytest-cov 리포트 |
| **타입 힌트 커버리지** | ~0% | 80%+ | mypy --strict 리포트 |
| **문서 최신성** | 2개월 지연 | 1주일 이내 | `PROJECTS_INDEX.md` 갱신 주기 |
| **빌드/테스트 성공률** | N/A | 95%+ | CI 파이프라인 성공률 |
| **평균 복구 시간(MTTR)** | 미측정 | < 30분 | 인시던트 로그 분석 |

---

## 🎯 요약: Top 3 즉시 액션

1. **🔴 시크릿 유출 차단** — 71_밀리이북, 25_auto_pobbagi, 65_android_apps 즉시 조치
2. **📝 문서 현실화** — PROJECTS_INDEX.md, NEXT_PROJECTS.md 최신 상태로 갱신
3. **🧪 테스트 기반 마련** — pytest 인프라 구축, 26_eval_pipeline부터 커버리지 확보

---

*이 리포트는 자동화된 코드 분석과 수동 리뷰를 병행하여 작성되었습니다.  
구체적인 구현 지원이나 우선순위 조정이 필요하면 말씀해 주세요.*