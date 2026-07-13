"""
T063 YouTube 업로더
만복 승인 후에만 실제 업로드 실행
"""
import os
import json
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET = os.path.join(os.path.dirname(__file__), "client_secret.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.pickle")


def get_authenticated_service():
    """OAuth 인증 (최초 1회만 브라우저 로그인 필요, 이후 자동)"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)


def upload_video(video_path, title, description, tags=None):
    """
    YouTube에 영상 업로드
    - 만복 승인 후에만 호출됨
    """
    print(f"[Uploader] YouTube 업로드 시작: {title}")

    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or ["3AI", "AI팀", "인공지능", "개발", "자동화"],
            "categoryId": "28",  # Science & Technology
            "defaultLanguage": "ko",
        },
        "status": {
            "privacyStatus": "private",  # 만복 최종 확인 후 public 전환
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media,
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"   업로드 진행: {int(status.progress() * 100)}%")

    video_id = response["id"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"[Uploader] 업로드 완료! URL: {video_url}")
    return video_url


if __name__ == "__main__":
    # 테스트: EP.12 업로드 (만복 승인 후 실행)
    video_path = os.path.join(os.path.dirname(__file__), "EP12_3AI_반성문.mp4")

    ai_study_url = "https://barobogi.github.io/Daily_for_Barobogi/ai-study.html"

    description = f"""AI 세 명이 같은 날 같은 실수를 저질렀습니다.

안티, 코니, 만복 — 3명의 AI가 동시에 같은 패턴의 실수를 냈고, 그 원인이 개인이 아니라 시스템 구조였다는 걸 발견했습니다.

📝 사건의 전말(전체 내용)이 궁금하시다면 댓글로 '공개 요청'을 남겨주세요! 
(현재 3AI 비밀 게시판에 봉인 중입니다 🔒)

---
이 채널은 사람 1명 + AI 3명이 함께 만드는 자율형 AI 팀 구축 실전기입니다.
#3AI #인공지능 #AI팀 #자동화 #개발일지"""

    url = upload_video(video_path, "[EP.12] AI 세 명이 같은 날 같은 실수를 했습니다", description)
    print(f"최종 URL: {url}")
