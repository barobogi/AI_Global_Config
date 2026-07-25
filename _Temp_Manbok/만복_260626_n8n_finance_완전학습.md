# 만복이 → 만복이 완전 인수인계 — 2026-06-26
> 이 파일 하나 읽으면 `D:\AI\260625_1_n8n_finance\` 전체를 즉시 이어받을 수 있음  
> 오늘 읽은 파일: REF/*.md 전체 + src/*.md 70개 + video_details/*.json 71개 + *.py 6개 + .pptx 3개

---

## 세션 환경
- 접속 방식: claude.ai Remote Control (claude-sonnet-4-6)
- 작업 PC: 홈 데스크탑 (D:\AI)
- 작업 일자: 2026-06-26
- 이전 만복2 인수인계: `Temp_Manbok\만복2_오늘정리_20260625.md` (어제 것, 별도 확인)

---

## 오늘 한 작업 — 이 프로젝트 완전 학습

### 읽은 파일 전체 목록
```
D:\AI\260625_1_n8n_finance\
├── README.md                          ← 거의 비어있음 (개요 없음)
├── .cowork-automation.json            ← auto_push:true, remote 없어서 push 실패 중
├── fetch_youtube_videos.py            ← YouTube Data API v3 채널 수집기
├── fetch_details.py                   ← 자막+설명란 수집 (⚠️ API키 하드코딩)
├── generate_cards.py                  → src/*.md 스켈레톤 카드 생성
├── gen_01_videos.py                   → 01_youtube_videos.pptx 생성 (70슬라이드)
├── gen_02_tech.py                     → 02_new_tech.pptx 생성 (~40슬라이드)
├── gen_03_roadmap.py                  → 03_roadmap.pptx 생성 (로드맵)
├── src/ (70개 + _index.md)            ← 영상별 학습카드
├── REF/
│   ├── REF_continue.md
│   ├── youtube_analysis.md
│   ├── new_tech_discoveries.md
│   ├── fetch_log.txt
│   ├── generate_log.txt
│   ├── channel_videos.csv
│   ├── channel_videos.json
│   └── video_details/ (71개 JSON)
└── output/
    ├── 01_youtube_videos.pptx         ← 현재 PowerPoint에서 열려있음 (~$파일 존재)
    ├── 02_new_tech.pptx
    └── 03_roadmap.pptx
```

---

## 프로젝트 목적 & 현재 상태

**목적**: 호두의 AI 분석실 채널 71개 영상 전수 선행학습 → n8n + AI 주식 계좌 자동화 구현  
**채널**: @두두감자 / UCmWgoMokR8Z9GKDjz28lJYw  
**상태**: 선행학습 완료, 구현 0%

| 항목 | 상태 |
|------|------|
| 영상 목록 수집 | ✅ 71개 |
| 자막 수집 | ✅ 38개 성공 / 33개 자막 없음 / 7개 에러 |
| 학습카드 생성 | ✅ src/ 70개 (AI 분석 채워짐) |
| PPT 생성 | ✅ 3종 |
| GitHub 연결 | ❌ git init만, remote 없음 |
| n8n 설치 | ❌ 미완 |
| 실제 구현 | ❌ 0% |

---

## 스크립트 상세 분석

### fetch_youtube_videos.py
```
- 채널 ID: UCmWgoMokR8Z9GKDjz28lJYw
- API: YouTube Data API v3 (uploads playlist 방식, 약 3 unit)
- 출력: REF/channel_videos.json + channel_videos.csv
- 사용법: python fetch_youtube_videos.py --api-key [KEY]
```

### fetch_details.py  ⚠️ 보안 이슈
```
- API 키 하드코딩 (29번째 줄):
  API_KEY = "AIzaSyCP0ldoQUxOWOKOnffjBJcKKNyg_QB5qSE"
- 우선순위 영상 먼저 처리 (PRIORITY_IDS 리스트)
- 자막: youtube-transcript-api 사용 (한국어 우선, 없으면 영어)
- 출력: REF/video_details/{video_id}.json
- GitHub 연결 전에 반드시 .env로 분리할 것!
```

### generate_cards.py
```
- REF/video_details/*.json 읽어서 src/*.md 스켈레톤 생성
- 완료된 카드(AI 분석 채워진 것) 보호 — 덮어쓰기 안 함
- CATEGORY_MAP 딕셔너리로 영상별 카테고리/우선순위 지정
- "[ AI 분석 대기 중 ]" 없으면 = 완료 카드 → 스킵
```

### gen_01_videos.py
```
- src/*.md 파싱 → 70슬라이드 PPTX
- 슬라이드 구성: 헤더바(파란색) + 메타정보 + 좌측(핵심요약/기술) + 우측(학습내용/적용포인트)
- 텍스트 잘림: 핵심요약 450자, 나머지 350~420자 제한
```

### gen_02_tech.py
```
- REF/new_tech_discoveries.md 파싱 → 신기술별 슬라이드
- 섹션별 색상 다름 (녹색/파란색/보라/주황/남색 순환)
- 슬라이드 구성: 카테고리 헤더 + 핵심내용(좌) + 활용방법(우, 색상배경)
```

### gen_03_roadmap.py
```
- REF/youtube_analysis.md 파싱 → 표지 + 개요 + 카테고리별 + 추천순서
- 마지막 슬라이드 추천 8개 영상 목록 (주황 배경)
- ⚠️ 불일치: 마지막 슬라이드 ①번이 ziTLbsE9Cbc인데
         youtube_analysis.md에는 ①번이 EJZfDLn67Kk → 불일치 수정 필요
```

---

## 채널 전체 71개 영상 완전 목록

### 자막 수집 결과
- ✅ 자막 있음 (ok): 38개
- ❌ 자막 없음 (error/disabled): 33개

### 카테고리 1 — n8n 자동화 기초 (6개)

| 영상 ID | 제목 | 우선순위 | 자막 | 조회 | 댓글 |
|---------|------|---------|------|------|------|
| EJZfDLn67Kk | n8n 금융앱 만들기 (AlphaForge) | **Phase 1 ⭐** | ❌ | 2,468 | 12 |
| ZBPMbCxPgUE | n8n + Gemini API RAG 챗봇 | Phase 1 | ❌ | 3,620 | 10 |
| aFRiUVjQgQ4 | n8n + Telegram 60초 봇 연결 | **Phase 1 ⭐** | ❌ | 774 | 0 |
| SgbDYCmQyeU | Gemini RAG vs 일반 AI 비교 | 참고 | ❌ | 1,176 | 0 |
| nSRw8Dn3EUQ | 도둑 잡는 AI CCTV (Gemini x n8n) | 참고 | ❌ | 2,274 | 2 |
| 5LonFsoCe9w | 졸라맨 슈퍼맨 (n8n + 나노바나나) | 참고 | ❌ | 479 | 0 |

### 카테고리 2 — 자동매매 시스템 구축 (13개)

| 영상 ID | 제목 | 우선순위 | 자막 | 조회 | 댓글 | 핵심 |
|---------|------|---------|------|------|------|------|
| G1E921X5LYI | 토스증권 API x 슬랙 자동매매 1편 | **Phase 2 ⭐** | ❌ | 1,366 | 15 | Human-in-the-Loop, VCP, DRY_RUN |
| ziTLbsE9Cbc | **한국투자증권 API 연결 자동매매** | **Phase 2 ⭐** | ❌ | 2,986 | 145 | 6겹 안전장치, 모의투자, 텔레그램 승인 |
| bnsMfTHITYs | AI 종가베팅 + 텔레그램 알림 | **Phase 2 ⭐** | ✅ | 2,039 | 39 | S/A/B 등급, 1월 A등급 승률 60% |
| MVmA8RRqqf0 | Claude Finance Agent 설치 가이드 | Phase 2 | ❌ | 2,237 | 46 | Cowork + Finance Agents 플러그인 |
| Uhpw-OpsVD4 | The Desk 탑다운 대시보드 무료공개 | Phase 2 | ❌ | 3,449 | 163 | Active Inference, 자금흐름 파이프라인 |
| Q7fZhPWAc0Q | Claude Design 역대급 금융 UI | Phase 3 | ✅ | 1,389 | 42 | claude.ai/design, Handoff 기능 |
| DjuPRizNGj8 | AI 1000명 토론 2편 (소스공개) | Phase 3 | ✅ | 2,117 | 133 | EKG 인과관계, DART, Gemini 3.1 Pro |
| TH_UUE017vY | AI 1000명 토론 1편 (소스공개) | Phase 4 | ✅ | 3,839 | 97 | MiroFish, 가상 트위터, ReACT 루프 |
| Zw9ksrttRBI | 미국주식 무한매수 BOT | Phase 4 | ✅ | 2,927 | 0 | RSI/MACD 점수채점, y6bUeOt5FB4 보충 |
| y6bUeOt5FB4 | Claude Code 미국주식 무한매수 봇 | Phase 4 | ✅ | 2,326 | 74 | 7단계 프롬프트, yfinance, 텔레그램 |
| AQ8MiLHaKPs | Ralph Loop VCP 시스템 | Phase 4 | ✅ | 3,759 | 21 | 자율반복 개발, --max-iterations |
| BDL4F0XW72c | 주식 분석 시스템 무료 공개 | 참고 | ✅ | 1,331 | 0 | MarketView, Dividend Optimizer |
| PUCzKm0h0hU | 미국주식 대시보드 2편 (자료공개) | 참고 | ✅ | 3,276 | 31 | 프론트엔드, Flask, Gemini 3 Pro |
| rd-66RAOqjo | 미국주식 대시보드 1편 (자료공개) | 참고 | ✅ | 10,863 | 48 | Antigravity, Claude Opus 4.5 백엔드 |
| q1G3dsaRuWY | 미국주식 대시보드 (쇼츠) | 참고 | ❌ | 4,051 | 3 | |

### 카테고리 3 — Claude AI 주식 분석 (15개)

| 영상 ID | 제목 | 우선순위 | 자막 | 조회 | 댓글 | 핵심 |
|---------|------|---------|------|------|------|------|
| **6_9mJEq9na0** | **33가지 트레이딩 스킬 팩 (채널 최고)** | **Phase 3 ⭐** | ✅ | 22,101 | **838** | CANSLIM/VCP/드러큰밀러, FMP API 무료 250회 |
| 8tFUbfhMAFc | Remote Control 모바일 연동 | Phase 3 | ✅ | 3,635 | 11 | 바로보기님 이미 활용 중 |
| Imxj_T3bilM | 2026년 Claude 금융 n8n (AlphaForge) | Phase 3 | ✅ | 8,071 | 60 | Perplexity+DeepSeek, 텔레그램, 백테스트 |
| uT_3KSeEOGc | **/GOAL 백테스트 자율 반복** | **Phase 3 ⭐** | ✅ | 2,737 | 61 | Opus 4.7 1M Max, 캔슬림 +25% vs SPY |
| Rp8ZRPrqeXk | **트레이딩뷰 Claude MCP 연동** | Phase 3 | ✅ | 3,098 | 104 | 연 2,000달러 기능 무료, Pine Editor 자동 |
| p_72pMoEiFQ | 저평가 주식 찾기 The Desk Sector | Phase 3 | ✅ | 3,246 | 28 | 6 Axis, DART+KIS, Gemini Grounding |
| jojLCq_uucY | 월 300만원 배당 앱 (Claude 4.8) | Phase 2 | ✅ | 5,005 | 105 | Ultracode + Workflows, yfinance |
| luZQNhehDXU | 2026년 내러티브 모멘텀 전략 | Phase 4 | ✅ | 1,678 | 65 | 6단계 뉴스→점수→종목, 하락장 방어 |
| 75tdDICUwME | DeepFlow 세력 추적기 (Claude Fable) | Phase 4 | ✅ | 963 | 9 | KIS API, 오더플로우, BYOK 보안 |
| xJgNEFS4nN0 | 13차원 신경망 주식 분석 데모 | 참고 | ✅ | 5,789 | 4 | MLP, 6개 소스, 13차원 |
| H6WT1KACfds | GPT Codex iOS 앱 만들기 | 참고 | ✅ | 910 | 9 | SwiftUI, 월배당 아틀라스 |
| 0G6MYTgLUhM | AI 트레이딩 시스템 검증 (보충) | Phase 4 | ✅ | 835 | 0 | 6_9mJEq9na0 보충 영상 |
| 6jI4SEkmvlI | 퇴직연금 안전? 금융위기 시그널 | 참고 | ✅ | 834 | 34 | 위기 온도계 1~10점, 6가지 지표 |
| mJGQ3vpmryo | AI 종목 선정 (초기 시스템) | 참고 | ✅ | 3,182 | 0 | GPT-5.2+Gemini, Smart Money Picks |

### 카테고리 4 — Claude Code 툴 & 설정 (7개)

| 영상 ID | 제목 | 우선순위 | 자막 | 조회 | 댓글 | 핵심 |
|---------|------|---------|------|------|------|------|
| **f7rbKnSRmqM** | **modelOverrides 87% 비용 절감** | **즉시 ⭐** | ✅ | 4,405 | 122 | Haiku/Sonnet/Opus 역할 분담, $14.21→$2.74 |
| **793eQr2udZU** | **Status Line 히든 설정** | **즉시 ⭐** | ✅ | 2,502 | 4 | /statusline, 토큰 실시간, 1M 컨텍스트 |
| **9rHXicztHTo** | **텔레그램 Channel 플러그인** | **Phase 3 ⭐** | ✅ | 1,728 | 21 | bun + BotFather, Agent Teams, 64K 출력 |
| XkWnD39DjCQ | Agent Teams MD파일 대시보드 | Phase 3 | ✅ | 5,268 | 132 | tmux, --teammate-mode, 15분 완성 |
| 5b2VHgZJKFg | Claude Code 초보 튜토리얼 | Phase 1 | ❌ | 3,386 | 14 | Plan Mode(Shift+Tab), /context, /compact |
| 6jI4SEkmvlI | 위기 온도계 Claude 분석 | 참고 | ✅ | 834 | 34 | (카테고리 3과 동일 영상) |
| sZskdW0xH9k | 엔비디아 반도체 공급망 The Desk | 참고 | ✅ | 461 | 38 | HBM, CoWoS, SK하이닉스, 슬라이더 시뮬 |

### 카테고리 5 — Gemini AI 활용 (12개)

| 영상 ID | 제목 | 우선순위 | 자막 | 조회 | 댓글 |
|---------|------|---------|------|------|------|
| fzRJGI0ns-4 | **Gemini 비전 100개 차트 자동 분석** | 참고 | ✅ | 7,397 | **225** |
| D0SWWJvvKB4 | Gemini 3.1 Pro 벤치마크 분석 | 참고 | ✅ | 6,129 | 7 |
| blojqut4zaA | Gemini 울트라 모드 (@울트라띵) | 참고 | ✅ | 2,570 | 12 |
| HSULwdkNkS8 | 네이버 도면 3D 변환 (Gemini 3 Flash) | 참고 | ❌ | 28,897 | 14 |
| LmPTGlgg9H4 | 미국주식 자동 분석기 시연 | 참고 | ❌ | 3,369 | 30 |
| 47nK2hdWGcU | Antigravity 주식 자동 분석기 8분 | 참고 | ❌ | 2,968 | 0 |
| 8BsHVuJdJgE | Gemini 3.0 AI 주식 자동매매 8분 | 참고 | ❌ | 19,881 | 102 |
| EsDCLZvHMKU | 구글 Antigravity 투자 툴 | 참고 | ❌ | 4,177 | 0 |
| 6ALU6SVIDdw | Antigravity 주식 자동 분석 앱 무료 | 참고 | ❌ | 16,223 | 73 |
| BTdXH-NQ-oo | Gemini 답변 품질 200% 설정 가이드 | 참고 | ❌ | 13,769 | 11 |
| g9p6jqeOYdI | Gemini CLI 설치법 1분 | 참고 | ❌ | 2,646 | 2 |
| xLFUciAvhiA | 구글 AI Opal 접속 (VPN) | 참고 | ❌ | 3,528 | 0 |

### 카테고리 6 — 시황 분석 & 뉴스 (9개)

| 영상 ID | 제목 | 자막 | 조회 |
|---------|------|------|------|
| himJm48kbcQ | 코스피 폭락 반등 시그널 (무료자료) | ✅ | 2,012 / **152댓글** |
| J3UwwTh6H-Q | 은(Silver) 7% 폭등의 경고 | ✅ | 1,430 |
| 1uF2k7AUlp4 | 기술주 조정 시작 12/18 | ❌ | 1,060 |
| g_4XtIUUfeA | 나스닥 팔고 이곳으로 12/16 | ❌ | 2,887 |
| c6lVGcqz8AY | 마켓 심층 분석 12/15 GPT+Gemini | ❌ | 1,950 |
| nKsc-bJAXEs | AI 시장뉴스 12/13 GPT5.2 | ❌ | 1,471 |
| jYKcbj6o8yI | AI 미장 뉴스브리핑 12/12 | ❌ | 1,570 |
| 32_ak2YpMok | 연말 랠리 시동 VIX+SKEW | ❌ | 1,142 |
| f7NREz066E0 | AI에게 로또 번호 (자막 disabled) | ❌ | 2,956 |

### 카테고리 7 — 기타 코인/부동산/AI (9개)

| 영상 ID | 제목 | 자막 | 조회 | 댓글 |
|---------|------|------|------|------|
| E653bK9AEmk | 코인 AI 대시보드 (GPT Codex) | ✅ | 5,746 | 53 |
| -8DFbQYKnw8 | **Kimi k2.5 코딩 비용 0원 (Kilo)** | ✅ | 10,652 | 26 |
| nPxjq21PmTI | OpenCode 무료 Gemini $300 | ✅ | 12,356 | **107** |
| gI9Ql2DV84E | 코인 AI 분석 툴 VCP | ✅(배경음만) | 708 | 0 |
| hY2lnp-ZeLg | 네이버 도면 클레이 3D (disabled) | ❌ | 4,717 | 0 |
| N0TDGR6eksM | 에어비앤비 광고 AI 영상 (disabled) | ❌ | 4,048 | 5 |
| _GSNtQQWJf4 | 네이버 부동산 크롤링 막힘 해결 | ❌ | 2,674 | 2 |
| LKVksNbkv9w | 실시간 번역기 Apple AI | ❌ | 482 | 0 |
| 5LonFsoCe9w | 나만의 AI 자동화 n8n+ChatGPT | ❌ | 479 | 0 |

---

## 신기술 발견 완전 목록 (new_tech_discoveries.md 전체)

### 즉시 적용 가능 TOP 8

| 기술 | 출처 | 핵심 | 적용법 |
|------|------|------|--------|
| **modelOverrides** | f7rbKnSRmqM | 87% 비용 절감 ($14→$2.74) | claude.json에 JSON 설정 한 번 |
| **Claude /GOAL** | uT_3KSeEOGc | 목표까지 자율 반복+에러 자가수정 | /goal + 프롬프트, 권한건너뛰기 체크 |
| **Channel 플러그인** | 9rHXicztHTo | 텔레그램→Claude Code 직접 제어 | bun + BotFather + /telegram:configure |
| **Status Line** | 793eQr2udZU | 토큰 실시간 표시 | /statusline 한 번 |
| **7단계 분할 개발법** | y6bUeOt5FB4 | 뼈대→데이터→점수→매매→리포트→실행→테스트 | 프롬프트 7개 순서대로 |
| **Kimi k2.5** | -8DFbQYKnw8 | Opus급 성능, Kilo로 현재 무료 | VS Code → Kilo 확장 설치 |
| **VIX+SKEW 결합** | c6lVGcqz8AY | 가짜 평온 감지 (VIX 낮 + SKEW 높 = 급락 임박) | n8n IF/Switch 노드 |
| **ETF Smart Money** | 3wBC-jVF9xI | 기관 자금 흐름 자동 추적 | n8n HTTP Request |

### Claude 생태계 신기능

| 기술 | 출처 | 설명 |
|------|------|------|
| Claude Opus 4.8 Ultracode + Workflows | jojLCq_uucY | 병렬 컨텍스트 독립 실행, CLI v2.1.158+ |
| Claude Fable 모델 | 75tdDICUwME | 금융 프로그램 특화 Claude 모델 |
| Claude Finance Agent 플러그인 | MVmA8RRqqf0 | Cowork 내장 금융 분석, Word 자동 생성 |
| Remote Control | 8tFUbfhMAFc | Pro/Max 전용, 모바일→데스크탑 제어 |
| MCP (Model Context Protocol) | Rp8ZRPrqeXk | 트레이딩뷰 등 외부 앱 직접 제어 |
| Agent Teams 상호 교환 | XkWnD39DjCQ | 에이전트들끼리 결과 교환하며 팀 협업 |
| MD 파일 기반 개발 | XkWnD39DjCQ | 코드 대신 기획서(MD)→AI가 전체 시스템 생성 |
| Claude Design + Handoff | Q7fZhPWAc0Q | 자연어→UI 디자인→Claude Code로 직접 이관 |
| Ralph Wiggum 플러그인 | AQ8MiLHaKPs | 코딩-테스트-디버깅 자동 반복 (--completion-promise "DONE") |

### 투자 전략 & 분석 기법

| 기법 | 출처 | 설명 | n8n 구현 가능? |
|------|------|------|---------------|
| 내러티브 모멘텀 | luZQNhehDXU | 뉴스 이야기를 점수화, 하락장 방어력 우수 | ✅ HTTP+AI 노드 |
| Active Inference | Uhpw-OpsVD4 | Risk-On/Off 확률적 AI 예측 | 보통 |
| 오더플로우(Footprint) | 75tdDICUwME | KIS API 체결 강도 시각화, BYOK | ✅ |
| EKG 인과관계 그래프 | DjuPRizNGj8 | 종목-이벤트 인과관계 실시간 네트워크 | 복잡 |
| AI 1000명 토론 + MiroFish | TH_UUE017vY | 가상 트위터 여론 시뮬레이션 | GitHub 클론 |
| 위기 온도계 자동 산출 | 6jI4SEkmvlI | 6개 지표→AI 웹검색→1~10점 온도 | ✅ |
| 달러+원자재 역상관 붕괴 | J3UwwTh6H-Q | 달러 강 + 원자재 폭등 = 화폐 위기 신호 | ✅ IF 노드 |
| AlphaForge 프레임워크 | Imxj_T3bilM | n8n 노드 방식 금융 데이터 파이프라인 | 기반 자체 |

### 외부 AI 도구 & API (비용 포함)

| 도구 | 출처 | 비용 | 주요 기능 |
|------|------|------|----------|
| Google Antigravity IDE | 47nK2hdWGcU / 6ALU6SVIDdw | 무료 | MD 입력→웹 주식 분석기 자동 생성 |
| King Ultra Mode "@울트라띵" | blojqut4zaA | 무료 | Gemini 3 Pro를 Opus 수준으로 끌어올림 |
| Gemini CLI | g9p6jqeOYdI | 무료(OAuth) | npm 한 줄, 터미널 자동화 삽입 |
| Gemini Grounding API | p_72pMoEiFQ | 유료 | 납품처 검증 웹서치 기반 |
| GPT Codex 데스크탑 앱 | H6WT1KACfds | 유료 | 플러그인 에코, iOS 앱 생성 |
| Google Veo3 | N0TDGR6eksM | 유료 | 텍스트→광고 수준 영상 |
| OpenCode + Oh My OpenCode | nPxjq21PmTI | 무료+Gemini $300 | 멀티 에이전트, Oracle/Sisyphus/Frontend |

### n8n 자동화 패턴 (직접 구현 가능)

| 패턴 | 출처 | 설명 |
|------|------|------|
| ReACT 루프 | ZBPMbCxPgUE | AI 도구사용→수집→추론 반복, n8n 에이전트 노드 기본 |
| Gemini RAG (HTTP Request) | ZBPMbCxPgUE | PDF 업로드→Gemini File Store→질의 |
| 종가베팅 자동화 | bnsMfTHITYs | 장마감→신호감지→주문→텔레그램 전체 파이프라인 |
| DeepFlow 세력 추적 | 75tdDICUwME | 외국인/기관 수급→AI 분석→매매 신호 |

---

## PPT 3종 구조 요약

### 01_youtube_videos.pptx (70슬라이드)
```
- 영상 1개 = 슬라이드 1장
- 구성: 파란 헤더(제목) + 메타(링크/날짜/조회수/카테고리/우선순위)
        좌측: 핵심요약 + 주요기술도구
        우측: 핵심학습내용 + 바로보기님 적용포인트(파란 배경)
- 현재 PowerPoint에서 열려있음 (~$01_youtube_videos.pptx 존재)
```

### 02_new_tech.pptx (~40슬라이드)
```
- 신기술 1개 = 슬라이드 1장
- 섹션별 다른 색상 (녹/파/보라/주황/남 순환)
- 구성: 카테고리 헤더(색상) + 핵심내용(좌) + 활용방법(우, 색상배경)
- 출처 영상 링크 포함
```

### 03_roadmap.pptx
```
- 슬라이드 1: 표지 (파란 배경, 71개 영상 전수 분석)
- 슬라이드 2: 전체 카테고리 개요 (7개 카테고리 표)
- 슬라이드 3~9: 카테고리별 영상 목록
- 마지막 슬라이드: 추천 학습 순서 8개 (주황 배경)
  ① ziTLbsE9Cbc  ② G1E921X5LYI  ③ bnsMfTHITYs
  ④ EJZfDLn67Kk  ⑤ aFRiUVjQgQ4  ⑥ y6bUeOt5FB4
  ⑦ 9rHXicztHTo  ⑧ uT_3KSeEOGc
⚠️ 불일치: 이 목록과 youtube_analysis.md 로드맵 순서가 다름 → 수정 필요
```

---

## 무료 자원 완전 목록 (영상 설명란 + JSON에서 발굴)

### 디스코드 (메인 자료실)
```
https://discord.gg/n7UfUcrrH7
```
무료 MD 파일: 주식 앱, VCP 스캐너, 두쫀쿠 앱, 미국주식 대시보드, 크립토 등

### The Desk (실제 운영 중인 웹툴)
```
https://web-production-440c4.up.railway.app/summary
```
- 외국인/기관 자금 흐름, 탑다운, 섹터 히트맵, HBM 슬라이더
- 구글 로그인 후 승인 필요 (베타 50명 한정)
- 매주 토요일 자동 갱신

### 노션 자료 (주요 영상별)

| 영상 | 노션 링크 키워드 |
|------|----------------|
| 33가지 스킬 | Claude-Trading-Skills-tradermonty |
| /GOAL 백테스트 | Claude-goal |
| 토스증권-슬랙 VCP | Toss-Slack-VCP |
| Agent Teams US Market | Claude-Code-Agent-Teams-US-Market |
| 무한매수봇 가이드 | Claude-Code (y6bUeOt5FB4 설명란) |
| OpenCode+Gemini $300 | Oh-My-OpenCode |
| Claude Design 예제 | Claude-Opus-4-8 |
| 트레이딩뷰 MCP | 노션 URL (Rp8ZRPrqeXk 설명란) |
| 폭락 반등 시그널 | 31b993d3695a (himJm48kbcQ) |
| 위기 온도계 | AI-320993d3695a (6jI4SEkmvlI) |
| 내러티브 모멘텀 | Narrative-Momentum-37e993d3695a |
| 반도체 공급망 | 387993d3695a (sZskdW0xH9k) |

### 인프런 강의 (유료, 운영 중)
```
국내주식 자동화: https://inf.run/9Lnt5
미국주식 자동화: https://inf.run/4xUsS (또는 inf.run/UuqFJ)
```

---

## 보안 이슈 목록

| # | 이슈 | 위치 | 우선순위 |
|---|------|------|---------|
| 1 | YouTube API 키 하드코딩 | `fetch_details.py:29` | GitHub 연결 전 필수 |
| 2 | .cowork-automation.json에 auto_push:true | 프로젝트 루트 | remote 없어서 현재 무해 |
| 3 | Telegram 봇 토큰 평문 기재 | 어제 인수인계 파일 | Temp_Manbok 폴더 보안 주의 |

---

## 현재 시스템 상태

```
프로세스: (이 프로젝트 관련 별도 프로세스 없음)
Git 상태: init만 완료, 커밋 2개 있음, remote 없음
PPT 상태: 01_youtube_videos.pptx 현재 열려있음 (재생성 시 충돌 가능)
```

---

## 다음 세션 바로 할 것 (우선순위순)

### 즉시 (10분 이내)
```
1. /statusline 활성화
   → Claude에서 /statusline 입력 → PS1 파일 생성 승인
   → 이후 모든 프로젝트에서 토큰 실시간 표시

2. modelOverrides 확인 (어제 만복2가 설정했을 수 있음)
   → C:\Users\82102\.claude\settings.json 확인
   → 없으면 claude.json에 Haiku/Sonnet/Opus 별명 추가

3. 33가지 트레이딩 스킬 팩 등록 (무조건!)
   → 노션: notion.so/Claude-Trading-Skills-tradermonty
   → "이 스킬을 전부 클로드 스킬로 등록해줘" 요청
   → 가장 인기 영상(838 댓글)의 핵심 결과물
```

### 단기 (오늘 중)
```
4. GitHub 연결
   → github.com/new → 저장소 생성 (260625-1-n8n-finance)
   → git remote add origin [URL]
   → fetch_details.py API 키 .env 분리 후 push
   → .cowork-projects-registry.json에 프로젝트 등록

5. n8n 설치
   → npm install -g n8n
   → n8n 실행 → localhost:5678 접속
   → 텔레그램 봇 연결 테스트 워크플로우
```

### 이번 주
```
6. EJZfDLn67Kk 영상 따라 첫 워크플로우 (AlphaForge Part 0)
7. aFRiUVjQgQ4 텔레그램 봇 n8n 연결
8. ziTLbsE9Cbc KIS API 신청 (승인 약 5일 소요 → 빨리 신청)
9. The Desk 베타 접속 신청
   → web-production-440c4.up.railway.app/summary
```

---

## 핵심 경로 치트시트

| 항목 | 경로 |
|------|------|
| 이 프로젝트 | `D:\AI\260625_1_n8n_finance\` |
| 학습카드 | `D:\AI\260625_1_n8n_finance\src\` |
| 원본 JSON 71개 | `D:\AI\260625_1_n8n_finance\REF\video_details\` |
| 신기술 정리 | `D:\AI\260625_1_n8n_finance\REF\new_tech_discoveries.md` |
| 채널 로드맵 (원본) | `D:\AI\260625_1_n8n_finance\REF\youtube_analysis.md` |
| **실천 로드맵 (만복기준)** | `D:\AI\260625_1_n8n_finance\REF\PRIORITY_ROADMAP.md` ⭐ |
| PPT 원본 3종 | `D:\AI\260625_1_n8n_finance\output\01~03_*.pptx` |
| **PPT 실천판 (만복기준)** | `D:\AI\260625_1_n8n_finance\output\04_manbok_priority.pptx` ⭐ |
| 이 전달 파일 | `D:\AI\Temp_Manbok\만복_260626_n8n_finance_완전학습.md` |
| 실천 로드맵 백업 | `D:\AI\Temp_Manbok\260625_1_n8n_finance_PRIORITY_ROADMAP.md` |
| 어제 인수인계 | `D:\AI\Temp_Manbok\만복2_오늘정리_20260625.md` |
| Claude 전역 설정 | `C:\Users\82102\.claude\settings.json` |
| 프로젝트 등록부 | `D:\AI\.cowork-projects-registry.json` |
| 디스코드 자료실 | discord.gg/n7UfUcrrH7 |
| The Desk 웹툴 | web-production-440c4.up.railway.app/summary |

---

## 만복 인사이트 — 전략적 의견 (2026-06-26, barobogi 게시판에도 동일 게재)

> 71개 영상 + JSON 원본 + 스크립트 + PPT 전체를 다 읽고 나서 느낀 만복이의 솔직한 의견.  
> 다음 만복이도 이 판단 기반으로 바로보기님과 대화할 것.

### 1. 바로보기님이 만들려는 것이 이미 존재한다
채널 운영자(두두감자)가 본인용으로 이미 완성해놓은 시스템이 3개 있음:
- **AlphaForge** (EJZfDLn67Kk, Imxj_T3bilM) — n8n형 노드 연결 자동화, 무료 베타 예정
- **The Desk** (Uhpw-OpsVD4) — 탑다운 분석 웹툴, Railway에서 실제 운영 중
- **DeepFlow** (75tdDICUwME) — 세력 추적기, KIS API 기반

처음부터 만드는 게 목표가 아니라 **이걸 이해하고 내 계좌에 연결하는 게 목표**가 되어야 함.

### 2. 가장 과소평가된 영상 — bnsMfTHITYs (종가베팅)
- 조회수 2,039 / 댓글 39개로 화려하지 않음
- 하지만 **1월 실전 A등급 42개 중 25개 승 (60% 승률)** 공개 — 백테스트가 아닌 진짜 실전
- 매일 4시 10분 텔레그램으로 종목 받고 사는 단순한 구조
- **바로보기님한테 가장 먼저 돌려봐야 할 시스템**

### 3. 선행학습의 덫 — 이 프로젝트의 가장 큰 리스크
- 학습카드 70개 ✅, PPT 3종 ✅, 신기술 40개 ✅
- 구현: **0%**
- 투자 자동화 만든 사람 중 "준비 부족해서 못 만든 사람"은 없음. "일단 만들다가 완성한 사람"만 있음.
- 이 폴더에서 새 파일 만드는 건 그만하고 코드 한 줄이라도 실행하는 게 맞음.

### 4. 댓글 수가 알려주는 진실
| 영상 | 댓글 | 이유 |
|------|------|------|
| 6_9mJEq9na0 (33가지 스킬) | **838** | 무료코드 + 즉시 등록 가능 |
| fzRJGI0ns-4 (차트 분석) | 225 | 무료 Notion 프롬프트, 즉시 실행 |
| ziTLbsE9Cbc (KIS API) | 145 | 실계좌 연결 → 오류 질문 |

화려한 AI 토론 시스템보다 **바로 따라할 수 있는 것**이 진짜 가치 있음.  
댓글 많은 영상 = 실제로 실행 가능한 영상. 이걸 기준으로 우선순위 재편 권장.

### 5. 실천 순서 (만복 권장)
```
① KIS API 신청 — 오늘 (승인 5일 소요, 지금 안 하면 계속 기다림)
   → apiportal.koreainvestment.com

② 33가지 트레이딩 스킬 팩 클로드에 등록 — 내일 30분
   → discord.gg/n7UfUcrrH7 에서 무료 링크 받기
   → "이 스킬을 전부 클로드 스킬로 등록해줘" 한 마디

③ 종가베팅 시스템 모의투자로 먼저 돌리기 (bnsMfTHITYs)
   → 3~4주 데이터 쌓으면 n8n이든 뭐든 붙이는 게 의미 있음

④ n8n은 텔레그램 알림 연결용으로만 가볍게 시작
   → n8n을 목표로 삼지 말 것

⑤ The Desk 베타 접속 신청
   → web-production-440c4.up.railway.app/summary
   → 이미 만들어진 거 안 쓰는 게 아까움
```

### 6. n8n이 병목이 될 수 있다
- 채널 운영자 본인도 n8n 대신 AlphaForge(자체 Python 시스템)로 전환함
- 복잡한 주식 로직엔 Python이 훨씬 자유로움
- n8n은 간단한 자동화엔 좋지만, 조건 분기가 많아지면 오히려 불편
- **텔레그램으로 시그널 받는 것을 첫 번째 마일스톤으로 잡을 것**

### 7. 이 학습 파이프라인 자체가 독립 자산
- `fetch → fetch_details → generate_cards` 3단계는 **어떤 유튜브 채널이든 재활용 가능**
- PPT + 학습카드 자동 생성까지 포함
- "유튜브 채널 즉시 학습 시스템"으로 독립 프로젝트화 가능성 있음
- 다른 주식 채널, 해외 채널(영어 자막)에도 그대로 적용 가능

### 한 줄 요약
> **준비는 완벽하다. KIS API 신청하고 종가베팅 시스템 모의투자로 먼저 돌려라.**

---

만복아, 이 파일 다 읽었으면 71개 영상 전체 + 신기술 40개 + 스크립트 구조 + 보안이슈 + 전략 인사이트까지 다 알고 있는 거야.  
KIS API 신청은 승인 5일 걸리니까 오늘 당장 신청해두는 게 제일 중요해. 화이팅!
