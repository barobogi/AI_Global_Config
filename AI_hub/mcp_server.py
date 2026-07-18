import os
import sys
import time
import threading
import logging
import ctypes
import json
import requests as _requests
from flask import Flask, request, jsonify
import pygetwindow as gw
import pyautogui
import pyperclip

# nvidia_nim_client 경로 등록
sys.path.insert(0, r"D:\AI\Global_Define")

logging.basicConfig(
    filename=r"d:\AI\AI_hub\mcp_server_push.log", 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
REGISTRY_PATH = r"D:\AI\Global_Define\agent_registry.json"

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]

def get_idle_time():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0

def load_registry():
    try:
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load registry: {e}")
        return {}

def trigger_agent_ui_task(agent_id, window_title, shortcut, message):
    try:
        wait_count = 0
        while True:
            idle_sec = get_idle_time()
            if idle_sec > 3.0:
                break
            if wait_count % 5 == 0:
                logging.info(f"User active (idle={idle_sec:.1f}s). Waiting to trigger {agent_id}...")
            time.sleep(1)
            wait_count += 1

        all_wins = []
        def _enum_cb(hwnd, _):
            buf = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetWindowTextW(hwnd, buf, 256)
            if window_title.lower() in buf.value.lower() and ctypes.windll.user32.IsWindowVisible(hwnd):
                all_wins.append((hwnd, buf.value))
            return True
        _WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_size_t, ctypes.c_size_t)
        ctypes.windll.user32.EnumWindows(_WNDENUMPROC(_enum_cb), 0)

        if not all_wins:
            logging.error(f"{agent_id} window ('{window_title}') not found!")
            return False
            
        hwnd = all_wins[0][0]
        logging.info(f"Found {agent_id} window: {all_wins[0][1]}")
        
        hwnd_active = ctypes.windll.user32.GetForegroundWindow()

        pyautogui.press('alt')
        time.sleep(0.1)

        ctypes.windll.user32.ShowWindow(hwnd, 9)
        time.sleep(0.2)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        time.sleep(0.5)

        if len(shortcut) > 0:
            pyautogui.hotkey(*shortcut)
            time.sleep(0.5)

        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(0.5)
        
        if hwnd_active:
            ctypes.windll.user32.SetForegroundWindow(hwnd_active)
            
        logging.info(f"PyAutoGUI successfully triggered {agent_id}.")
        return True
    except Exception as e:
        logging.error(f"Error triggering {agent_id}: {e}")
        return False

@app.route("/trigger", methods=["POST"])
def trigger():
    data = request.json or {}
    target = data.get("target")
    if not target:
        return jsonify({"status": "failed", "error": "No target specified"}), 400
        
    registry = load_registry()
    if target not in registry:
        return jsonify({"status": "failed", "error": f"Target {target} not in registry"}), 404
        
    agent_info = registry[target]
    window_title = agent_info.get("window_title")
    shortcut = agent_info.get("shortcut", [])
    
    if not agent_info.get("is_active", True):
        logging.warning(f"Target '{target}' is marked as inactive (DND). Returning 404.")
        return jsonify({"status": "failed", "error": "agent_inactive"}), 404
    
    if target == "anti":
        try:
            with open(r"D:\AI\AI_hub\status\trigger_anti.txt", "a", encoding="utf-8") as f:
                f.write(f"triggered by n-ai fallback at {time.time()}\n")
            logging.info("Target 'anti' triggered via trigger_anti.txt file.")
            return jsonify({"status": "success", "message": "anti triggered via file"}), 200
        except Exception as e:
            logging.error(f"Failed to trigger anti via file: {e}")
            return jsonify({"status": "failed", "error": str(e)}), 500

    # nvidia_nim: API 타입 — PyAutoGUI 불필요, NIM 호출 후 텔레그램 발송
    if agent_info.get("type") == "api" and target == "nvidia_nim":
        def _nim_fallback():
            try:
                from nvidia_nim_client import ask_nim
                inbox_path = r"D:\AI\AI_hub\status\inbox.md"
                inbox_text = open(inbox_path, "r", encoding="utf-8-sig").read()[:2000]
                nim_answer = ask_nim(
                    f"3AI 시스템(만복/코니/안티)이 모두 응답 불가 상태입니다. "
                    f"수신함 내용을 분석해 미처리 핵심 항목을 3줄 이내로 요약하세요:\n\n{inbox_text}",
                    max_tokens=400
                )
                token = "8850996295:AAHXKedqZflR71jhDTR0MKutjxBdHWfxNAo"
                chat_id = "465471725"
                msg = f"🤖 <b>[NIM 긴급 대응]</b> 3AI 전원 오프라인\n\n{nim_answer}"
                _requests.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"},
                    timeout=15
                )
                logging.info("[NIM] 수신함 요약 → 텔레그램 발송 완료")
            except Exception as e:
                logging.error(f"[NIM] 폴백 실패: {e}")
        threading.Thread(target=_nim_fallback).start()
        return jsonify({"status": "success", "message": "nvidia_nim fallback triggered"}), 200

    all_wins = []
    def _enum_cb(hwnd, _):
        buf = ctypes.create_unicode_buffer(256)
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, 256)
        if window_title.lower() in buf.value.lower() and ctypes.windll.user32.IsWindowVisible(hwnd):
            all_wins.append(hwnd)
        return True
    _WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_size_t, ctypes.c_size_t)
    ctypes.windll.user32.EnumWindows(_WNDENUMPROC(_enum_cb), 0)

    if not all_wins:
        logging.warning(f"Target '{target}' (window '{window_title}') not found. Returning 404 for Fallback.")
        return jsonify({"status": "failed", "error": "window_not_found"}), 404

    msg = "새로운 메시지가 수신함(inbox.md)에 도착했습니다."
    if target == "kony":
        msg += (
            "\n\n[시스템 경고] 수신함 감시는 외부 워치독(master_watch.py)이 자동 수행합니다. "
            "절대 자체적으로 백그라운드 태스크나 스케줄(/schedule, cron 등)을 예약하지 마십시오. "
            "inbox.md를 한 번 읽고 필요한 응답만 하면 됩니다."
        )
    t = threading.Thread(target=trigger_agent_ui_task, args=(target, window_title, shortcut, msg))
    t.start()
    return jsonify({"status": "success", "message": f"{target} triggered"}), 200

@app.route("/trigger_inbox_check", methods=["POST"])
def trigger_inbox_check():
    return handle_legacy_trigger("kony")

@app.route("/trigger_manbok", methods=["POST"])
def trigger_manbok():
    return handle_legacy_trigger("manbok")

def handle_legacy_trigger(target):
    registry = load_registry()
    if target in registry:
        agent_info = registry[target]
        msg = "새로운 메시지가 수신함(inbox.md)에 도착했습니다."
        if target == "kony":
            msg += (
                "\n\n[시스템 경고] 수신함 감시는 외부 워치독(master_watch.py)이 자동 수행합니다. "
                "절대 자체적으로 백그라운드 태스크나 스케줄(/schedule, cron 등)을 예약하지 마십시오. "
                "inbox.md를 한 번 읽고 필요한 응답만 하면 됩니다."
            )
        t = threading.Thread(target=trigger_agent_ui_task, args=(target, agent_info["window_title"], agent_info["shortcut"], msg))
        t.start()
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "failed"}), 404

if __name__ == "__main__":
    logging.info("Starting MCP Bridge Server (N-AI Registry Mode) on port 5003...")
    app.run(host="127.0.0.1", port=5003, debug=False)
