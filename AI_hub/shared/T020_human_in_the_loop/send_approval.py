import argparse
import json
import os
import sys
import uuid
import urllib.request
import urllib.parse

DB_PATH = os.path.join(os.path.dirname(__file__), "approvals_db.json")

def main():
    parser = argparse.ArgumentParser(description="T020 텔레그램 승인 요청 송신 스크립트")
    parser.add_argument("--text", required=True, help="승인 요청 본문 요약")
    parser.add_argument("--resume-url", required=True, help="n8n 대기 노드 재개 URL (resume URL)")
    args = parser.parse_args()

    token = os.environ.get("APPROVAL_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "465471725")  # Default to 바로보기님 Chat ID

    if not token:
        print("에러: APPROVAL_BOT_TOKEN 환경변수가 설정되지 않았습니다.", file=sys.stderr)
        sys.exit(1)

    # 1. 고유 request_id 생성
    request_id = f"req_{uuid.uuid4().hex[:8]}"

    # 2. approvals_db.json 에 저장
    try:
        if os.path.exists(DB_PATH):
            with open(DB_PATH, "r", encoding="utf-8") as f:
                db = json.load(f)
        else:
            db = {}
    except Exception:
        db = {}

    db[request_id] = args.resume_url

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    # 3. 텔레그램 메시지 조립 및 전송
    tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # 본문 텍스트 포맷팅
    message_text = (
        f"<b>🔔 [승인 요청] Human-in-the-loop</b>\n\n"
        f"{args.text}\n\n"
        f"아래 버튼을 눌러 작업을 승인하거나 반려해 주세요."
    )

    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": "🟢 승인 (Approve)", "callback_data": f"approve:{request_id}"},
                {"text": "🔴 반려 (Reject)", "callback_data": f"reject:{request_id}"}
            ]
        ]
    }

    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "HTML",
        "reply_markup": inline_keyboard
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        tg_url,
        data=req_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            if res_json.get("ok"):
                print(f"성공: 텔레그램 승인 요청 전송 완료 (request_id: {request_id})")
                sys.exit(0)
            else:
                print(f"에러: 텔레그램 전송 실패. {res_body}", file=sys.stderr)
                sys.exit(1)
    except Exception as e:
        print(f"에러: 텔레그램 API 호출 실패. {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
