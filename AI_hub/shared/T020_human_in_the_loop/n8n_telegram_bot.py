import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

DB_PATH = os.path.join(os.path.dirname(__file__), "approvals_db.json")

def tg_api_call(token, method, payload):
    url = f"https://api.telegram.org/bot{token}/{method}"
    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=req_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=35) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"[{datetime.now()}] Telegram API Error ({method}): {e}", file=sys.stderr)
        return None

def apply_t022_patch(patch_info: dict, action: str) -> bool:
    """T022 패치 직접 적용 (승인 시 파일 쓰기 + git push)"""
    if action != "approve":
        print(f"[{datetime.now()}] T022 패치 반려됨: {patch_info.get('local_path', '?')}")
        return True

    local_path = patch_info.get("local_path", "")
    code = patch_info.get("code", "")
    cwd = patch_info.get("cwd", str(Path(local_path).parent) if local_path else ".")

    if not local_path or not code:
        print(f"[{datetime.now()}] T022 패치 정보 불완전 (local_path 또는 code 없음)", file=sys.stderr)
        return False

    try:
        Path(local_path).write_text(code, encoding="utf-8")
        print(f"[{datetime.now()}] T022 패치 적용 완료: {local_path}")
    except Exception as e:
        print(f"[{datetime.now()}] T022 파일 쓰기 실패: {e}", file=sys.stderr)
        return False

    try:
        subprocess.run(["git", "add", local_path], cwd=cwd, check=True, capture_output=True)
        alert_name = patch_info.get("alert_name", "보안 취약점")
        subprocess.run(
            ["git", "commit", "-m", f"fix(security): T022 자동 패치 — {alert_name}"],
            cwd=cwd, check=True, capture_output=True
        )
        subprocess.run(["git", "push"], cwd=cwd, check=True, capture_output=True)
        print(f"[{datetime.now()}] T022 git push 완료: {cwd}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] T022 git 작업 실패: {e}", file=sys.stderr)
        return False


def resume_n8n(resume_url, action):
    req_data = json.dumps({"action": action}).encode("utf-8")
    req = urllib.request.Request(
        resume_url,
        data=req_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.getcode()
            print(f"[{datetime.now()}] n8n resume request status: {status}")
            return status in (200, 201)
    except Exception as e:
        print(f"[{datetime.now()}] n8n resume failed: {e}", file=sys.stderr)
        return False

def main():
    token = os.environ.get("APPROVAL_BOT_TOKEN")
    if not token:
        print("에러: APPROVAL_BOT_TOKEN 환경변수가 설정되지 않았습니다.", file=sys.stderr)
        sys.exit(1)

    print(f"[{datetime.now()}] T020 승인 봇 데몬 시작...")
    offset = 0

    while True:
        try:
            # 1. 텔레그램 업데이트 가져오기 (롱폴링 30초)
            payload = {"offset": offset, "timeout": 30}
            updates = tg_api_call(token, "getUpdates", payload)
            
            if not updates or not updates.get("ok"):
                time.sleep(2)
                continue

            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                
                # callback_query 가 존재하는지 확인 (인라인 버튼 클릭)
                if "callback_query" in update:
                    callback = update["callback_query"]
                    callback_id = callback["id"]
                    data = callback.get("data", "")
                    message = callback.get("message", {})
                    chat_id = message.get("chat", {}).get("id")
                    message_id = message.get("message_id")
                    original_text = message.get("text", "")

                    if not data or ":" not in data:
                        continue

                    action, request_id = data.split(":", 1)
                    print(f"[{datetime.now()}] 승인 신호 수신 - Action: {action}, Request ID: {request_id}")

                    # approvals_db.json 에서 요청 정보 조회
                    db_entry = None
                    if os.path.exists(DB_PATH):
                        try:
                            with open(DB_PATH, "r", encoding="utf-8") as f:
                                db = json.load(f)
                            db_entry = db.get(request_id)
                        except Exception as e:
                            print(f"DB 읽기 실패: {e}", file=sys.stderr)

                    if not db_entry:
                        tg_api_call(token, "answerCallbackQuery", {
                            "callback_query_id": callback_id,
                            "text": "⚠️ 만료되었거나 찾을 수 없는 요청입니다.",
                            "show_alert": True
                        })
                        continue

                    # T022 패치 직접 적용 vs n8n resume 분기
                    is_t022 = isinstance(db_entry, dict) and db_entry.get("type") == "t022"
                    if is_t022:
                        success = apply_t022_patch(db_entry, action)
                    else:
                        success = resume_n8n(db_entry, action)

                    if success:
                        # 텔레그램 스피너 해제
                        action_ko = "승인" if action == "approve" else "반려"
                        tg_api_call(token, "answerCallbackQuery", {
                            "callback_query_id": callback_id,
                            "text": f"✅ 성공적으로 {action_ko} 처리되었습니다."
                        })

                        # 메시지 수정 (버튼 제거 및 상태 업데이트)
                        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        status_icon = "🟢" if action == "approve" else "🔴"
                        
                        # 기존 메시지 본문에서 하단 안내 문구 제거하고 상태 문구 추가
                        lines = original_text.split("\n")
                        # "아래 버튼을 눌러..." 문구 제거 시도
                        filtered_lines = [l for l in lines if "아래 버튼을 눌러" not in l]
                        body_text = "\n".join(filtered_lines).strip()

                        updated_text = (
                            f"{body_text}\n\n"
                            f"{status_icon} <b>[처리 완료]</b>\n"
                            f"이 요청은 <b>{action_ko}</b> 되었습니다. ({now_str})"
                        )

                        tg_api_call(token, "editMessageText", {
                            "chat_id": chat_id,
                            "message_id": message_id,
                            "text": updated_text,
                            "parse_mode": "HTML",
                            "reply_markup": {"inline_keyboard": []}  # 버튼 제거
                        })

                        # 사용이 완료된 request_id는 DB에서 제거
                        try:
                            with open(DB_PATH, "r", encoding="utf-8") as f:
                                db = json.load(f)
                            if request_id in db:
                                del db[request_id]
                            with open(DB_PATH, "w", encoding="utf-8") as f:
                                json.dump(db, f, ensure_ascii=False, indent=2)
                        except Exception as e:
                            print(f"DB 업데이트 실패: {e}", file=sys.stderr)

                    else:
                        tg_api_call(token, "answerCallbackQuery", {
                            "callback_query_id": callback_id,
                            "text": "❌ n8n 서버 연결에 실패했습니다. (나중에 다시 시도)",
                            "show_alert": True
                        })

                # T024 VibeCoding 및 일반 메시지 수신 (N-AI 레지스트리 기반 동적 라우팅)
                elif "message" in update and "text" in update["message"]:
                    message = update["message"]
                    chat_id = message.get("chat", {}).get("id")
                    text = message.get("text", "")
                    
                    if text.strip() and chat_id:
                        text_lower = text.lower()
                        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                        messages_dir = r"D:\AI\AI_hub\shared\messages"
                        registry_path = r"D:\AI\Global_Define\agent_registry.json"
                        
                        # 1. VibeCoding 명시적 호출
                        if "/vibe" in text_lower or "바이브" in text_lower:
                            print(f"[{datetime.now()}] T024 VibeCoding 명령 수신: {text[:20]}...")
                            script_path = r"D:\AI\64_vibecoding\generator_trigger.py"
                            if os.path.exists(script_path):
                                subprocess.Popen(
                                    [sys.executable, script_path, str(chat_id), text],
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL,
                                    cwd=r"D:\AI\64_vibecoding"
                                )
                            else:
                                tg_api_call(token, "sendMessage", {
                                    "chat_id": chat_id,
                                    "text": "❌ VibeCoding 생성기 스크립트를 찾을 수 없습니다."
                                })
                            continue

                        # 2. N-AI 레지스트리 기반 동적 라우팅
                        try:
                            with open(registry_path, "r", encoding="utf-8") as f:
                                registry = json.load(f)
                        except Exception as e:
                            print(f"레지스트리 로드 실패: {e}")
                            registry = {}

                        target_agent = None
                        target_name = None
                        fallback_agent = None
                        fallback_name = None
                        fallback_priority_val = 999

                        for agent_id, data in registry.items():
                            current_priority = data.get("fallback_priority", 999)
                            if current_priority < fallback_priority_val:
                                fallback_priority_val = current_priority
                                fallback_agent = agent_id
                                fallback_name = data.get("name", agent_id)
                                
                            for kw in data.get("keywords", []):
                                if kw.lower() in text_lower:
                                    target_agent = agent_id
                                    target_name = data.get("name", agent_id)
                                    break
                            if target_agent:
                                break

                        if not target_agent:
                            target_agent = fallback_agent
                            target_name = fallback_name

                        if target_agent:
                            print(f"[{datetime.now()}] {target_name}({target_agent}) 지시 수신: {text[:30]}...")
                            title = "유튜브 동영상 뽀개기(T063) 요청" if "youtu" in text_lower else "사용자 텔레그램 지시사항"
                            msg_filename = f"바로보기→{target_name}_{now_str}_텔레그램지시.md"
                            msg_path = os.path.join(messages_dir, msg_filename)
                            content = f"status: unread\n\n# {title}\n\n{text}"
                            
                            with open(msg_path, "w", encoding="utf-8") as f: 
                                f.write(content)
                            
                            subprocess.Popen([sys.executable, r"D:\AI\Global_Define\push_to_all.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=r"D:\AI\Global_Define")
                            tg_api_call(token, "sendMessage", {"chat_id": chat_id, "text": f"✅ {target_name}에게 전달했습니다. (수신함 등록 및 알람 완료)"})
                        else:
                            tg_api_call(token, "sendMessage", {"chat_id": chat_id, "text": "❌ 라우팅 대상을 찾을 수 없으며 폴백 에이전트도 없습니다."})

        except Exception as e:
            print(f"[{datetime.now()}] 메인 루프 예외 발생: {e}", file=sys.stderr)
            time.sleep(5)

if __name__ == "__main__":
    main()
