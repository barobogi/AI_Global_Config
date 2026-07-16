# YouTube OAuth 최초 설정 (1회만)

## 1단계: Google Cloud Console

1. https://console.cloud.google.com 접속
2. 새 프로젝트 생성: `3AI-YouTube`
3. API 및 서비스 → 라이브러리 → `YouTube Data API v3` → 사용 설정
4. API 및 서비스 → 사용자 인증 정보
   → OAuth 2.0 클라이언트 ID 만들기
   → 애플리케이션 유형: 데스크톱 앱
   → 이름: `3AI-Upload`
5. JSON 다운로드 → 파일명을 `client_secret.json`으로 변경
6. `D:\AI\63_youtube_creator\pipeline\client_secret.json` 에 저장

## 2단계: 최초 인증 (1회)

```powershell
cd "D:\AI\63_youtube_creator\pipeline"
C:\hb\python.exe youtube_upload.py --file "test.mp4" --title "test" --type shorts --privacy private
```

→ 브라우저 열림 → Google 계정 로그인 → 허용
→ `youtube_token.json` 자동 생성 (이후 자동 재사용)

## 3단계: 승인+업로드 사용법

```powershell
# 안티 1차 승인
python approve_and_upload.py --video crisp_dm_shorts.mp4 --title "CRISP-DM 데이터분석 6단계" --type shorts --stage 1 --ai 안티 --ok

# 코니 2차 승인
python approve_and_upload.py --video crisp_dm_shorts.mp4 --title "CRISP-DM 데이터분석 6단계" --type shorts --stage 2 --ai 코니 --ok

# 만복 3차 승인 → 자동 업로드 시작
python approve_and_upload.py --video crisp_dm_shorts.mp4 --title "CRISP-DM 데이터분석 6단계" --type shorts --stage 3 --ai 만복 --ok
```

반려 시:
```powershell
python approve_and_upload.py --video crisp_dm_shorts.mp4 --title "..." --stage 1 --ai 안티 --reject --note "음성 품질 낮음, 재렌더링 필요"
```
