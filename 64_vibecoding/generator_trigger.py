import sys
import os
import json
import urllib.request
import threading
from app_generator import process_prompt
from port_manager import ensure_server_running

def tg_send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=req_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            pass
    except Exception as e:
        print(f"Failed to send telegram message: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python generator_trigger.py <chat_id> <prompt>")
        sys.exit(1)

    chat_id = sys.argv[1]
    prompt = sys.argv[2]
    app_name = "3ai_dashboard"
    
    token = os.environ.get("APPROVAL_BOT_TOKEN")
    
    # Send initial status
    if token:
        tg_send_message(token, chat_id, "⏳ VibeCoding 진행 중... 코드를 생성하고 있습니다.")

    # Timeout mechanism
    def timeout_handler():
        if token:
            tg_send_message(token, chat_id, "⚠️ 생성 지연 (Timeout) - 5분이 초과되어 강제 종료되었습니다. 로그를 확인하세요.")
        os._exit(1)
        
    timer = threading.Timer(300, timeout_handler)  # 5 minutes
    timer.start()

    try:
        # Generate code
        result_type = process_prompt(app_name, prompt)
        
        # Start server if needed
        port = ensure_server_running(app_name)
        
        # Respond
        if token:
            url = f"http://localhost:{port}"
            if result_type == "whitelist":
                msg = f"🎨 피드백(CSS) 즉시 반영 완료!\n확인: {url}"
            else:
                msg = f"✅ 웹앱 생성이 완료되었습니다!\n주소: {url}"
            tg_send_message(token, chat_id, msg)
            
    except Exception as e:
        if token:
            tg_send_message(token, chat_id, f"❌ 에러 발생: {e}")
        print(f"Error: {e}")
    finally:
        timer.cancel()

if __name__ == "__main__":
    main()
