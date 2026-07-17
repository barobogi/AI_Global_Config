# anti_watchdog.py — 안티 트리거 감시 + 텔레그램 알림 (2026-07-18 개선)
import os
import sys
import time
import json
import urllib.request
from pathlib import Path

TRIGGER_FILE = r"D:\AI\AI_hub\status\trigger_anti.txt"
INBOX_PATH   = r"D:\AI\AI_hub\status\inbox.md"
TOKEN        = "8850996295:AAHXKedqZflR71jhDTR0MKutjxBdHWfxNAo"
CHAT_ID      = "465471725"


def send_telegram(msg: str):
    try:
        payload = json.dumps({"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data=payload, headers={"Content-Type": "application/json"}, method="POST"
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass


def get_latest_trigger_content():
    try:
        lines = Path(TRIGGER_FILE).read_text(encoding="utf-8").strip().split("\n")
        return lines[-1] if lines else ""
    except Exception:
        return ""


def main():
    print("[Anti Watchdog] 시작 — trigger 감시 + 텔레그램 알림", flush=True)

    if not os.path.exists(TRIGGER_FILE):
        Path(TRIGGER_FILE).write_text("init\n", encoding="utf-8")

    last_mtime = os.path.getmtime(TRIGGER_FILE)

    # 시작 알림
    send_telegram("🤖 <b>Anti Watchdog</b> 시작됨\ntrigger_anti.txt 감시 중...")

    while True:
        time.sleep(1.0)
        try:
            current_mtime = os.path.getmtime(TRIGGER_FILE)
            if current_mtime > last_mtime:
                last_mtime = current_mtime
                content = get_latest_trigger_content()
                print(f"\n[Anti Trigger] 새 트리거: {content}", flush=True)

                # 텔레그램으로 안티에게 알림 (바로보기님 봇 통해 안티에게 전달)
                send_telegram(
                    f"🚨 <b>안티 새 작업 지시 도착!</b>\n"
                    f"<code>{content[:80]}</code>\n\n"
                    f"안티에게: <b>inbox.md 확인 후 즉각 대응하세요!</b>"
                )
        except Exception:
            pass


if __name__ == "__main__":
    main()
