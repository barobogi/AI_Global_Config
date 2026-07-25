# 바로보기님 맞춤 실천 로드맵
> 작성: 2026-06-26 | 기준: 만복 인사이트 (댓글 수 + 실전 검증 + 구현 난이도)  
> 이 파일은 채널 원본 순서(youtube_analysis.md)와 다릅니다 — 의도적으로 재편한 것입니다.

---

## 핵심 원칙 3가지

1. **원본은 이미 존재한다** — AlphaForge, The Desk, DeepFlow 모두 채널 운영자가 완성해놨음. 처음부터 만들 필요 없음.
2. **선행학습의 덫을 피할 것** — 학습카드 70개, PPT 3종, 신기술 40개 이미 완료. 이제는 실행만 남음.
3. **텔레그램 시그널 수신이 첫 번째 마일스톤** — n8n이 목표가 아님. "폰으로 시그널 받는 것"이 목표.

---

## 영상 학습 순서 (만복 기준)

### 🔴 오늘 당장 봐야 할 것 (이번 주)

| 순서 | 영상 ID | 제목 | 왜 먼저? |
|------|---------|------|---------|
| ① | `bnsMfTHITYs` | AI 종가베팅 자동화 + 텔레그램 | **실전 A등급 60% 승률 검증됨. 백테스트 아닌 진짜.** |
| ② | `ziTLbsE9Cbc` | 한국투자증권 API 연결 | **승인 5일 소요 → 오늘 신청 안 하면 계속 기다림.** |
| ③ | `6_9mJEq9na0` | 33가지 트레이딩 스킬 팩 | **댓글 838개 1위. 무료코드, 30분에 등록 가능.** |
| ④ | `f7rbKnSRmqM` | modelOverrides 87% 비용 절감 | **지금 당장 설정 하나로 월 25만원 절약.** |
| ⑤ | `793eQr2udZU` | Status Line 히든 설정 | **토큰 실시간 확인. /statusline 한 줄.** |

---

### 🟡 이번 달 봐야 할 것 (구현 병행)

| 순서 | 영상 ID | 제목 | 왜 이 순서? |
|------|---------|------|------------|
| ⑥ | `EJZfDLn67Kk` | n8n 금융앱 만들기 (AlphaForge) | 전체 파이프라인 구조 이해. 따라 만들 필요 없고 구조만 파악. |
| ⑦ | `aFRiUVjQgQ4` | n8n + Telegram 60초 봇 연결 | 가장 빠른 n8n 입문. Shorts라 짧음. |
| ⑧ | `G1E921X5LYI` | 토스증권 API x 슬랙 1편 | Human-in-the-Loop 구조 배우기. |
| ⑨ | `9rHXicztHTo` | 텔레그램 Channel 플러그인 | Claude Code에서 직접 텔레그램 제어. |
| ⑩ | `uT_3KSeEOGc` | Claude /GOAL 백테스트 | 전략 검증 자동화. 종가베팅 백테스트에 직접 적용 가능. |
| ⑪ | `Imxj_T3bilM` | 2026년 Claude 금융 n8n | AlphaForge 완성판 시연. Perplexity + DeepSeek + 텔레그램. |

---

### 🟢 나중에 봐도 되는 것 (시스템 고도화 후)

| 영상 ID | 제목 | 언제? |
|---------|------|-------|
| `luZQNhehDXU` | 내러티브 모멘텀 전략 | 종가베팅 3달 운영 후 고도화 시 |
| `75tdDICUwME` | DeepFlow 세력 추적기 | KIS API 연결 완료 후 |
| `TH_UUE017vY` | AI 1000명 토론 (MiroFish) | 관심용, 직접 구현은 나중 |
| `DjuPRizNGj8` | AI 1000명 토론 2편 | 위와 동일 |
| `p_72pMoEiFQ` | 저평가 주식 찾기 The Desk | The Desk 접속만 해도 됨 |
| `Rp8ZRPrqeXk` | 트레이딩뷰 MCP | 고급, 트레이딩뷰 유저일 때 |
| `XkWnD39DjCQ` | Agent Teams 대시보드 | 큰 시스템 만들 때 |

---

### ⛔ 지금 당장 볼 필요 없는 것

| 유형 | 해당 영상들 | 이유 |
|------|-----------|------|
| 시황 분석 뉴스 | 32_ak2YpMok, c6lVGcqz8AY 등 9개 | 단기 시황, 이미 지난 내용 |
| 부동산/코인 | hY2lnp-ZeLg, N0TDGR6eksM 등 | 목표와 무관 |
| Gemini 기초 | 47nK2hdWGcU, EsDCLZvHMKU 등 | Claude 기반으로 충분 |

---

## 구현 우선순위 (무엇부터 만들 것인가)

### 1단계: 텔레그램 시그널 수신 (목표: 2주 이내)
```
목표: "종목 시그널이 매일 폰으로 온다"
필요 영상: bnsMfTHITYs + aFRiUVjQgQ4
필요 도구: KIS API 모의투자 키 + BotFather 텔레그램 봇

체크리스트:
□ KIS Developers 가입 → 모의투자 신청
□ 텔레그램 BotFather에서 봇 생성
□ 종가베팅 시스템 Python으로 실행
□ 매일 4시 텔레그램으로 종목 수신 확인
```

### 2단계: 종가베팅 모의투자 검증 (목표: 1달)
```
목표: "내 데이터로 A등급 승률 직접 확인"
필요 영상: bnsMfTHITYs + uT_3KSeEOGc (/GOAL 백테스트)

체크리스트:
□ 3~4주 모의투자 시그널 기록
□ A등급 종목 실제 수익률 추적
□ /GOAL로 전략 백테스트 자동화
□ 승률 60% 이상이면 3단계 진행
```

### 3단계: KIS API 실계좌 연결 (목표: 2달)
```
목표: "소액으로 자동 매수 실행"
필요 영상: ziTLbsE9Cbc + G1E921X5LYI

체크리스트:
□ KIS API 실계좌 키 발급 (승인 후)
□ 텔레그램 버튼 승인 구조 구현 (Human-in-the-Loop)
□ 손절/익절 자동화 (-5% / +9%)
□ 일일 손실 한도 설정
□ 소액 테스트 (1~5만원/종목)
```

### 4단계: AlphaForge 수준 (목표: 3달+)
```
목표: "VCP + 수급 + AI 분석 + 텔레그램 전체 파이프라인"
필요 영상: EJZfDLn67Kk + Imxj_T3bilM + 9rHXicztHTo

체크리스트:
□ 종목 필터링 로직 추가 (VCP, 이평선)
□ 기관/외국인 수급 데이터 연동
□ DeepSeek/Perplexity API 뉴스 분석
□ 성과 대시보드 구축
```

---

## 즉시 활용 가능한 무료 자원

| 자원 | 접근법 | 가치 |
|------|--------|------|
| 디스코드 자료실 | discord.gg/n7UfUcrrH7 | 무료 MD 파일, 주식 앱 코드 다수 |
| The Desk 베타 | web-production-440c4.up.railway.app/summary | 탑다운 분석, 자금 흐름 실시간 |
| 33가지 스킬 노션 | 6_9mJEq9na0 설명란 링크 | 즉시 Claude에 등록 가능 |
| 종가베팅 가이드 | bnsMfTHITYs 설명란 노션 | 실전 시스템 그대로 따라 가능 |
| KIS API 포털 | apiportal.koreainvestment.com | 모의투자 먼저 신청 |
