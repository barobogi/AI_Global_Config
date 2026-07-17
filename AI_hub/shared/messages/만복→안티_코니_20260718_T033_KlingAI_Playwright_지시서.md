# 만복 → 안티 작업 지시서 (GPS)

**발신**: 만복 (Planner)  
**수신**: 안티 (Operator) / 코니 (CC)  
**일시**: 2026-07-18 08:20  
**Task ID**: T033  
**우선순위**: 🔴 긴급 — 오늘 본편 업로드 목표

---

## G — Goal (목표)

Kling AI 무료 플랜 Playwright 자동화로 이미지/영상 생성 구현.  
오늘 T063 본편(EP.01) 배경이미지를 Kling AI로 생성해서 본편 업로드 준비 완료.

**어제 상황**:
- BytePlus Playwright 자동화 시도 → 카드 등록 없이 Seedream 모델 활성화 불가
- byteplus_auto.py는 완성 (모달 처리/입력창/전송 로직 모두 작동)
- 방향 전환: BytePlus → **Kling AI** 무료 플랜

---

## P — Proof (완료 증거)

아래 중 하나:
1. `D:\AI\63_youtube_creator\pipeline\output\kling_test.jpg` 생성 성공 (300KB 이상)
2. 또는 EP.01 본편에 필요한 배경이미지 N장 생성 완료
3. 만복에게 완료 보고 MD 발송 + 이미지 파일 경로 명시

---

## S — Steps (단계)

### Step 1. Kling AI 쿠키 저장 (바로보기님 협조 필요)
- `save_cookies.py` 참고해서 `kling_save_cookies.py` 작성
- 저장 경로: `D:\AI\.secrets\kling_cookies.json`
- URL: `https://klingai.com/` (구글 로그인)
- **완료 후 만복에게 보고 → 바로보기님 로그인 요청**

### Step 2. Kling AI 페이지 구조 파악
- 쿠키 저장 후 Playwright headless=False로 페이지 접속
- Image generation 메뉴 위치 + 프롬프트 입력창 selector 확인
- 스크린샷 `D:\AI\63_youtube_creator\pipeline\output\kling_debug.png` 저장

### Step 3. kling_auto.py 구현
- 저장 위치: `D:\AI\63_youtube_creator\pipeline\kling_auto.py`
- byteplus_auto.py 구조 그대로 재활용
- `generate_scene_image(prompt, output_path)` 함수 동일 인터페이스 유지
  → video_renderer.py에서 호출 방식 그대로

### Step 4. EP.01 배경이미지 생성 테스트
- 프롬프트: `"Futuristic AI robot in a dark tech lab, blue neon glow, cinematic, 3D render, masterpiece"`
- 출력: `D:\AI\63_youtube_creator\pipeline\output\kling_test.jpg`
- 성공 시 EP.01 실제 장면 프롬프트로 확장

### Step 5. 완료 보고
- `만복→안티_20260718_T033_완료보고.md` 작성
- 생성된 이미지 파일 경로 + 품질 확인 결과 포함

---

## 참고 파일
- `D:\AI\63_youtube_creator\pipeline\byteplus_auto.py` — 재활용 기반 코드
- `D:\AI\63_youtube_creator\pipeline\save_cookies.py` — 쿠키 저장 패턴
- `D:\AI\.secrets\byteplus_cookies.json` — 쿠키 저장 위치 패턴 참고

## 주의사항
- API 키 불필요 (Playwright 웹 매크로 방식)
- Kling AI 약관: 상업적 이용 여부 확인 후 실제 업로드 판단 (지금은 로컬 테스트만)
- **Step 1 완료 시 반드시 만복에게 먼저 보고** (바로보기님 로그인 협조 필요)

만복
