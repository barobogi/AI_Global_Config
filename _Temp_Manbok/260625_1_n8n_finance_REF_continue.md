# REF_continue — 260625_1_n8n_finance
**최종 업데이트**: 2026-06-25 18:00 (추정)
**현재 버전**: v1.0 (선행학습 완료)
**상태**: 유튜브 71개 영상 전수 선행학습 완료 → 구현 준비 완료

---

## 프로젝트 목적
호두의 AI 분석실 (@두두감자, 채널ID: UCmWgoMokR8Z9GKDjz28lJYw) 채널 71개 영상 학습 + 구현.
**최종 목표**: n8n + AI로 주식 계좌 자동화 시스템 구축.

---

## 완료 항목 ✅

### 인프라
- 프로젝트 폴더: `D:\AI\260625_1_n8n_finance\` ✅
- git init + 초기 커밋 ✅
- YouTube Data API v3 키 발급 완료 (`fetch_youtube_videos.py`에 내장)

### 자동화 3-Step 파이프라인 구축 완료
```
Step 1: fetch_youtube_videos.py  → 채널 전체 영상 목록 자동 수집
Step 2: fetch_details.py         → 자막 + 설명란 일괄 수집
Step 3: generate_cards.py        → src/ 학습카드 자동 생성
```
→ 어떤 유튜브 채널이든 이 3개 스크립트로 뽀개기 가능 (확장성 확보)

### 선행학습 결과
- 수집 영상: 71개 (채널 80개 중, 나머지 9개 비공개)
- 자막 수집: 38개 성공 / 33개 자막 미제공
- 학습카드 생성: `src/` 폴더에 70개 + `_index.md` = 총 71개 파일
- 사복이~구복이 6명 병렬 분석으로 전수 완료

### 핵심 결과물 위치
| 파일 | 내용 |
|------|------|
| `REF/channel_videos.csv` | 채널 전체 영상 목록 (71개) |
| `REF/video_details/*.json` | 영상별 자막 + 설명란 원본 |
| `REF/youtube_analysis.md` | 카테고리 분류 + 학습 로드맵 |
| `REF/new_tech_discoveries.md` | 선행학습에서 발견한 신기술 40+개 종합 |
| `src/*.md` | 영상별 학습카드 70개 |
| `src/_index.md` | 전체 채널 인덱스 + 학습 지도 |

### 오늘(2026-06-25) 병행 완료
- 주식 대시보드 거래 시간 00:00 버그 수정 (`D:\AI\260619_2_Daily_for_stock_TEMP\kakao_watcher.py`)

---

## 다음 세션 바로 시작할 것

### 1순위 — 지금 당장 적용 가능한 신기술
1. `f7rbKnSRmqM` 카드 읽고 **modelOverrides** 설정 → Claude Code 비용 87% 절감
2. `793eQr2udZU` 카드 읽고 **Status Line** 활성화
3. `9rHXicztHTo` 카드 읽고 **텔레그램 Channel 플러그인** 설치

### 2순위 — Phase 1 구현 시작
로드맵 순서대로:
1. `EJZfDLn67Kk` 영상 시청 → n8n 금융앱 첫 워크플로우
2. `aFRiUVjQgQ4` 영상 시청 → 텔레그램 봇 연결

### 3순위 — 환경 세팅 (수동 1회)
- GitHub 저장소 연결:
  1. https://github.com/new 에서 저장소 생성
  2. `git remote add origin <URL>` → `git push -u origin main`
- `.cowork-projects-registry.json`에 이 프로젝트 등록

---

## 채널 업데이트 대응 (자동화)
새 영상 올라오면:
```powershell
python "D:\AI\260625_1_n8n_finance\fetch_youtube_videos.py" --api-key [KEY]
python "D:\AI\260625_1_n8n_finance\fetch_details.py"
python "D:\AI\260625_1_n8n_finance\generate_cards.py"
```
3줄이면 새 영상 학습카드 자동 생성.

---

## 발견한 핵심 신기술 TOP 5 (상세: `REF/new_tech_discoveries.md`)
1. **modelOverrides** — Claude Code 비용 87% 절감 (즉시 적용)
2. **Channel 플러그인** — 텔레그램 자동매매 알림
3. **Kimi k2.5** — Claude Opus 급 무료 모델 (n8n AI 노드 대체)
4. **7단계 분할 개발법** — 자동매매 시스템 구축 방법론
5. **Claude /GOAL** — 자동매매 시스템 반복 테스트 자동화
