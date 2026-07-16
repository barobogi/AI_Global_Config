# youtube_upload.py — YouTube Data API v3 자동 업로드 모듈
# 사용: python youtube_upload.py --file video.mp4 --title "제목" --type shorts
import os
import sys
import json
import argparse
import urllib.request
from pathlib import Path
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES          = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET   = Path(__file__).parent / "client_secret.json"
TOKEN_FILE      = Path(__file__).parent / "youtube_token.json"
CHANNEL_ID      = "UCxxxxxxxxxxxxxxxxxxxxx"  # 채널 등록 후 수정

TELEGRAM_TOKEN   = "8850996295:AAHXKedqZflR71jhDTR0MKutjxBdHWfxNAo"
TELEGRAM_CHAT_ID = "465471725"

CATEGORY_ID = "28"   # 과학기술


def _send_telegram(msg: str):
    try:
        payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data=payload, headers={"Content-Type": "application/json"}, method="POST",
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"텔레그램 알림 실패: {e}")


def _get_credentials() -> Credentials:
    """OAuth 인증 — 최초 1회 브라우저 인증, 이후 token.json 자동 재사용"""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                raise FileNotFoundError(
                    f"client_secret.json 없음: {CLIENT_SECRET}\n"
                    "Google Cloud Console → API 및 서비스 → 사용자 인증 정보 → OAuth 2.0 클라이언트 ID → JSON 다운로드"
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())

    return creds


def upload_video(
    file_path: str,
    title: str,
    description: str = "",
    tags: list[str] | None = None,
    video_type: str = "shorts",   # "shorts" | "main"
    privacy: str = "public",      # "public" | "unlisted" | "private"
) -> dict:
    """
    YouTube에 영상 업로드

    Returns:
        {"video_id": "...", "url": "https://youtu.be/...", "title": "..."}
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"영상 파일 없음: {file_path}")

    # 쇼츠는 제목에 #Shorts 추가
    if video_type == "shorts" and "#Shorts" not in title:
        title = f"{title} #Shorts"

    if not description:
        description = (
            f"바로보기의 3AI 연구소\n\n"
            f"만복(Claude Code CLI) + 코니(Cowork) + 안티(Antigravity) 3AI가 함께 만든 콘텐츠입니다.\n\n"
            f"#3AI #AI자동화 #{'쇼츠' if video_type == 'shorts' else '본편'}"
        )

    default_tags = ["3AI", "AI자동화", "만복", "코니", "안티", "바로보기의3AI연구소"]
    if tags:
        default_tags.extend(tags)

    print(f"[YouTube] 업로드 시작: {file_path.name}")
    print(f"[YouTube] 제목: {title}")
    print(f"[YouTube] 공개 설정: {privacy}")

    creds = _get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": default_tags[:15],
            "categoryId": CATEGORY_ID,
            "defaultLanguage": "ko",
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        str(file_path),
        chunksize=1024 * 1024,   # 1MB 청크
        resumable=True,
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"[YouTube] 업로드 중... {pct}%")

    video_id = response["id"]
    url = f"https://youtu.be/{video_id}"

    print(f"[YouTube] 업로드 완료: {url}")

    # 텔레그램 통보
    icon = "📱" if video_type == "shorts" else "🎬"
    _send_telegram(
        f"{icon} <b>유튜브 업로드 완료</b>\n"
        f"제목: {title.replace(' #Shorts', '')}\n"
        f"유형: {'쇼츠' if video_type == 'shorts' else '본편'}\n"
        f"링크: {url}"
    )

    return {"video_id": video_id, "url": url, "title": title}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube 자동 업로드")
    parser.add_argument("--file",    required=True, help="영상 파일 경로")
    parser.add_argument("--title",   required=True, help="영상 제목")
    parser.add_argument("--desc",    default="",   help="설명")
    parser.add_argument("--tags",    default="",   help="태그 (쉼표 구분)")
    parser.add_argument("--type",    default="shorts", choices=["shorts", "main"])
    parser.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"])
    args = parser.parse_args()

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    result = upload_video(
        file_path=args.file,
        title=args.title,
        description=args.desc,
        tags=tags,
        video_type=args.type,
        privacy=args.privacy,
    )
    print(f"\n업로드 완료: {result['url']}")
