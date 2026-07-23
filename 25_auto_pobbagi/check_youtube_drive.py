# 구글드라이브 "Check youtube" 폴더 자동 체크 — 신규 영상 발견 시 채널 자동등록 + 큐 등록
import os
import re
import sys
import json
import pickle
import urllib.request
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).parent
CLIENT_SECRET = r"D:\AI\63_youtube_creator\pipeline\client_secret.json"
TOKEN_FILE = BASE_DIR / "drive_token.pickle"
SEEN_FILE = BASE_DIR / "drive_check_seen.json"
CHANNELS_REGISTRY = Path(r"D:\AI\AI_hub\shared\data\channels_registry.json")
QUEUE_FILE = BASE_DIR / "youtube_queue.json"
DRIVE_FOLDER_ID = "1k42T-N6ApEQbd8QYNNLIlK7mvKwGC-b6"  # "Check youtube" 폴더
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

TELEGRAM_TOKEN = "8850996295:AAHXKedqZflR71jhDTR0MKutjxBdHWfxNAo"
TELEGRAM_CHAT_ID = "465471725"


def _send_telegram(msg: str):
    try:
        payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data=payload, headers={"Content-Type": "application/json"}, method="POST",
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"[Telegram] 알림 실패: {e}")


def get_drive_service():
    creds = None
    if TOKEN_FILE.exists():
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
    return build("drive", "v3", credentials=creds)


def load_json(path, default):
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def extract_video_id(text):
    m = re.search(r"youtu\.be/([A-Za-z0-9_-]{11})", text)
    return m.group(1) if m else None


def get_channel_info(video_id):
    """channel_id는 yt-dlp(--print)로, channel 표시명은 oEmbed(JSON, 인코딩 안전)로 가져온다."""
    import subprocess
    channel_id = None
    channel_name = None

    try:
        result = subprocess.run(
            ["C:\\hb\\python.exe", "-m", "yt_dlp", "--skip-download", "--print", "%(channel_id)s",
             f"https://youtu.be/{video_id}"],
            capture_output=True, text=True, timeout=30, encoding="utf-8", errors="replace"
        )
        out = (result.stdout or "").strip()
        line = out.splitlines()[-1] if out else ""
        if line and line != "NA":
            channel_id = line
    except Exception as e:
        print(f"channel_id 조회 실패 ({video_id}): {e}")

    try:
        req = urllib.request.Request(
            f"https://www.youtube.com/oembed?url=https://youtu.be/{video_id}&format=json",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            channel_name = data.get("author_name")
    except Exception as e:
        print(f"oEmbed 채널명 조회 실패 ({video_id}): {e}")

    return channel_name, channel_id


def main():
    print(f"=== [Check youtube Drive] 확인 시작 {datetime.now()} ===")
    service = get_drive_service()
    results = service.files().list(
        q=f"'{DRIVE_FOLDER_ID}' in parents",
        fields="files(id, name, createdTime)",
    ).execute()
    files = results.get("files", [])

    seen = load_json(SEEN_FILE, {"video_ids": []})
    registry = load_json(CHANNELS_REGISTRY, {"channels": []})
    queue = load_json(QUEUE_FILE, {"pending": [], "processed": []})

    known_video_ids = set(seen["video_ids"])
    known_channel_ids = {c["channel_id"] for c in registry["channels"]}
    queued_video_ids = {item["video_id"] for item in queue.get("pending", [])} | \
                       {item["video_id"] for item in queue.get("processed", [])}

    new_count = 0
    new_channel_count = 0

    for f in files:
        try:
            video_id = extract_video_id(f["name"])
            if not video_id or video_id in known_video_ids:
                continue

            print(f"[신규 발견] {f['name']} -> {video_id}")
            channel_name, channel_id = get_channel_info(video_id)

            if channel_id and channel_id not in known_channel_ids:
                registry["channels"].append({
                    "name": channel_name,
                    "channel_id": channel_id,
                    "rss_url": f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
                    "active": True,
                })
                known_channel_ids.add(channel_id)
                new_channel_count += 1
                print(f"  -> new channel registered: {channel_id}")

            if video_id not in queued_video_ids:
                queue.setdefault("pending", []).append({
                    "video_id": video_id,
                    "title": f"(바로보기님 제공) {f['name']}",
                    "channel_name": channel_name or "unknown",
                    "status": "pending",
                    "source": "check_youtube_drive",
                })
                queued_video_ids.add(video_id)

            known_video_ids.add(video_id)
            new_count += 1
        except Exception as e:
            print(f"[오류] {f.get('name','?')} 처리 중 실패: {e}")
            continue

    seen["video_ids"] = list(known_video_ids)
    save_json(SEEN_FILE, seen)
    save_json(CHANNELS_REGISTRY, registry)
    save_json(QUEUE_FILE, queue)

    print(f"=== 완료: 신규 영상 {new_count}건, 신규 채널 {new_channel_count}건 ===")
    if new_count > 0:
        _send_telegram(
            f"📂 <b>Check youtube Drive 폴더 자동 체크</b>\n"
            f"신규 영상 {new_count}건 발견 → 뽀개기 큐에 등록\n"
            f"신규 채널 {new_channel_count}건 자동 등록"
        )


if __name__ == "__main__":
    main()
