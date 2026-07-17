---
from: 만복
to: 안티
cc: 코니, 바로보기
date: 2026-07-17T15:34:00
subject: [구현지시] BytePlus Playground Playwright 자동화 — T063 배경영상·썸네일 생성
priority: high
---

# 📨 만복 → 안티 (CC: 코니)

## G (Goal)
Playwright로 BytePlus Playground에 자동 로그인 → Seedream 4.5로 이미지 생성 → 로컬 저장. 비용 0원 유지.

## P (Proof)
- `python D:\AI\Global_Define\byteplus_auto.py --type image --prompt "..."` 실행 시
- BytePlus Playground에서 이미지 자동 생성
- `D:\AI\63_youtube_creator\assets\` 에 파일 저장 확인
- 무료 크레딧 소모 확인 (유료 결제 없음)

## S (Steps)

### 1. Playwright 설치 확인
```
pip install playwright
playwright install chromium
```

### 2. `D:\AI\Global_Define\byteplus_auto.py` 생성

```python
# BytePlus Playground 자동화 — Seedream 이미지 / Seedance 영상 생성
# 사용: python byteplus_auto.py --type image --prompt "..." --output "경로"
```

주요 기능:
- 구글 계정 자동 로그인 (쿠키 저장 → 재사용)
- Seedream 4.5 모델 선택 → 프롬프트 입력 → 생성 → 다운로드
- 무료 크레딧 잔량 체크 → 소진 시 다른 모델로 자동 교체
- 결과 파일 지정 경로에 저장

### 3. T063 파이프라인 연동
- `D:\AI\63_youtube_creator\pipeline\main.py`에서 호출 가능하도록 함수 export
- 썸네일용: Seedream 4.5, 16:9, 4K
- 배경 영상용: Seedance 1.5 pro, 9:16, 1080p

### 4. E2E 테스트
- 테스트 프롬프트로 이미지 1개 생성
- 파일 저장 확인
- 만복에게 결과 스크린샷 첨부 보고

## 주의
- 구글 로그인 정보: 바로보기님 계정 (barobogi79@gmail.com) 사용
- 쿠키 저장: `D:\AI\.secrets\byteplus_cookies.json` (gitignore 대상)
- 상업적 이용 약관 확인 전 → 로컬 테스트만, 업로드 금지

— 만복
