# 오늘뭐하지 — 백엔드 서버 무료 상시 배포 가이드

본 문서는 Android 앱과 실시간 통신할 수 있는 FastAPI 백엔드를 **비용 0원(무료)** 또는 **초간편 방식**으로 상시 배포하는 3가지 방법을 설명합니다.

---

## 🌟 추천 1: Render.com (가장 추천 / 비용 0원 / 원클릭 클라우드)

GitHub 저장소와 연동하여 자동으로 HTTPS URL을 발급받는 가장 대중적인 무료 클라우드 호스팅 방식입니다.

### 배포 순서
1. [Render.com](https://render.com) 무료 회원가입 (GitHub 계정으로 로그인).
2. 대시보드에서 **`New +` ➔ `Web Service`** 클릭.
3. 내 GitHub 저장소(`AI` 또는 `today_what_to_do`) 선택.
4. 설정값 입력:
   - **Name**: `today-what-to-do-api`
   - **Root Directory**: `65_android_apps/today_what_to_do/backend`
   - **Runtime**: `Python 3` (또는 `Docker`)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free` 선택
5. **`Create Web Service`** 클릭.
6. 약 2분 후 생성되는 고유 HTTPS URL (예: `https://today-what-to-do-api.onrender.com`) 확인.

---

## 🚇 추천 2: Cloudflare Tunnel (내 PC/홈서버 활용 / 무제한 무료 / 초고속)

내 컴퓨터에서 FastAPI를 띄워두고, 포트포워딩이나 고정 IP 없이 Cloudflare를 통해 안전한 무료 HTTPS 주소를 생성하는 방식입니다.

### 실행 방법
1. [Cloudflare Tunnel (cloudflared)](https://github.com/cloudflare/cloudflared/releases) 다운로드.
2. 백엔드 실행:
   ```bash
   cd 65_android_apps/today_what_to_do/backend
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```
3. 터미널에서 즉시 공개 HTTPS URL 발급:
   ```bash
   cloudflared tunnel --url http://localhost:8000
   ```
4. 터미널에 출력되는 `https://xxxx.trycloudflare.com` 주소를 즉시 앱에 연동.

---

## 🐳 추천 3: Docker Compose 로컬/VPS 배포

개인 VPS(가상 서버)나 상시 켜두는 PC에서 도커로 안정적으로 백그라운드 구동할 때 사용합니다.

```bash
cd 65_android_apps/today_what_to_do/backend
docker-compose up -d --build
```
- 상태 확인: `docker ps`
- 로그 확인: `docker logs -f today_what_to_do_api`

---

## 📱 안드로이드 앱에 서버 주소 연동하기

배포 후 발급받은 URL을 아래 파일에 입력하면 앱이 실제 서버와 통신합니다:
- **파일 위치**: [`android/app/src/main/java/com/barobogi/todaywhattodo/data/network/RetrofitClient.kt`](file:///d:/AI/65_android_apps/today_what_to_do/android/app/src/main/java/com/barobogi/todaywhattodo/data/network/RetrofitClient.kt)
- **수정 내용**:
  ```kotlin
  // 배포된 서버 주소로 BASE_URL 변경 (끝에 / 필수)
  private const val BASE_URL = "https://today-what-to-do-api.onrender.com/"
  ```
