import argparse
import json
import os
import sys
import uuid
import urllib.request
import urllib.parse
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "approvals_db.json")

def main():
    parser = argparse.ArgumentParser(description="T020 텔레그램 승인 요청 송신 및 상태 관리 스크립트")
    parser.add_argument("--text", required=True, help="승인 요청 본문 요약")
    parser.add_argument("--resume-url", help="n8n 대기 노드 재개 URL (resume URL)")
    parser.add_argument("--patch-json", help="T022 패치 적용 정보 JSON 파일 경로 (resume-url 없이 동작)")
    parser.add_argument("--edit-timeout", action="store_true", help="타임아웃 자동 반려 메시지 편집 모드")
    parser.add_argument("--chat-id", help="메시지 편집 시 필요한 Chat ID")
    parser.add_argument("--message-id", help="메시지 편집 시 필요한 Message ID")
    args = parser.parse_args()

    token = os.environ.get("APPROVAL_BOT_TOKEN")
    if not token:
        print("에러: APPROVAL_BOT_TOKEN 환경변수가 설정되지 않았습니다.", file=sys.stderr)
        sys.exit(1)

    if args.edit_timeout:
        # 타임아웃 메시지 편집 모드
        if not args.chat_id or not args.message_id:
            print("에러: --edit-timeout 모드에서는 --chat-id와 --message-id가 필수입니다.", file=sys.stderr)
            sys.exit(1)

        tg_url = f"https://api.telegram.org/bot{token}/editMessageText"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 본문 조립 (HTML 태그 제거 방지 및 본문 유지)
        updated_text = (
            f"<b>🔔 [승인 요청] Human-in-the-loop</b>\n\n"
            f"{args.text}\n\n"
            f"🔴 <b>[승인 대기 시간 초과]</b>\n"
            f"이 요청은 24시간 내에 응답이 없어 <b>자동 반려</b>되었습니다. ({now_str})"
        )

        payload = {
            "chat_id": args.chat_id,
            "message_id": args.message_id,
            "text": updated_text,
            "parse_mode": "HTML",
            "reply_markup": {"inline_keyboard": []}  # 버튼 제거
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
                    print(json.dumps({"status": "success", "mode": "timeout_edit", "message_id": args.message_id}))
                    sys.exit(0)
                else:
                    print(f"에러: 텔레그램 메시지 수정 실패. {res_body}", file=sys.stderr)
                    sys.exit(1)
        except Exception as e:
            print(f"에러: 텔레그램 API 호출 실패. {e}", file=sys.stderr)
            sys.exit(1)

    else:
        # 일반 승인 요청 송신 모드
        if not args.resume_url:
            print("에러: 일반 모드에서는 --resume-url이 필수입니다.", file=sys.stderr)
            sys.exit(1)

        chat_id = os.environ.get("TELEGRAM_CHAT_ID", "465471725")

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

        # 3. 텔레그램 메시지 전송
        tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
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
                    # n8n이 캡처할 수 있도록 JSON 문자열 출력
                    output_data = {
                        "status": "success",
                        "request_id": request_id,
                        "chat_id": chat_id,
                        "message_id": res_json["result"]["message_id"],
                        "text": args.text
                    }
                    print(json.dumps(output_data))
                    sys.exit(0)
                else:
                    print(f"에러: 텔레그램 전송 실패. {res_body}", file=sys.stderr)
                    sys.exit(1)
        except Exception as e:
            print(f"에러: 텔레그램 API 호출 실패. {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
