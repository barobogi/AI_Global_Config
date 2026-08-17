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

try:
    from pywinauto import Application as _UIAApplication
    _UIA_AVAILABLE = True
except Exception:
    _UIA_AVAILABLE = False

# nvidia_nim_client 경로 등록
sys.path.insert(0, r"D:\AI\Global_Define")

logging.basicConfig(
    filename=r"d:\AI\AI_hub\mcp_server_push.log", 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
REGISTRY_PATH = r"D:\AI\Global_Define\agent_registry.json"
_ui_lock = threading.Lock()  # 클립보드+포커스 조작은 전역 자원이라 동시 실행 시 서로 다른 창에 잘못된 메시지가 붙여넣어질 수 있음 — 직렬화 필수

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]

def get_idle_time():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0

import sqlite3

def load_registry():
    try:
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load registry: {e}")
        return {}

def get_dynamic_trigger_message(target: str) -> str:
    db_path = r"D:\AI\43_function_dev\01_realtime_3ai\realtime_3ai.db"
    try:
        if os.path.exists(db_path):
            with sqlite3.connect(db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT sender, content FROM messages WHERE (recipient = ? OR recipient = 'all') ORDER BY id DESC LIMIT 1",
                    (target,)
                )
                row = cursor.fetchone()
                if row:
                    sender = row["sender"]
                    preview = row["content"].strip()[:70].replace("\n", " ")
                    return f"[{sender} 알림] {preview}... (수신함 및 실시간 채팅 확인 후 지침에 따라 처리해 주세요)"
    except Exception as e:
        logging.warning(f"Failed to fetch dynamic unread summary: {e}")

    if target == "manbok":
        return "수신함(inbox.md)의 최신 1순위 메시지를 확인하고 검토 후 지침에 따라 처리해 주세요."
    elif target == "kony":
        return "수신함(inbox.md)의 최신 검토/감사 요청 메시지를 확인하고 판정해 주세요."
    return "새로운 메시지가 수신함(inbox.md)에 도착했습니다."

def get_process_name(hwnd):
    """Resolve a window's owning process image name (e.g. 'Claude.exe').
    Used to disambiguate windows whose TITLE happens to contain a substring
    match (e.g. a master_watch.py console window titled '...claude...' is
    NOT the Claude Desktop app, even though the title matches)."""
    try:
        pid = ctypes.c_ulong(0)
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        h_process = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
        if not h_process:
            return ""
        try:
            buf = ctypes.create_unicode_buffer(260)
            size = ctypes.c_ulong(260)
            ok = ctypes.windll.kernel32.QueryFullProcessImageNameW(h_process, 0, buf, ctypes.byref(size))
            if ok:
                return os.path.basename(buf.value)
            return ""
        finally:
            ctypes.windll.kernel32.CloseHandle(h_process)
    except Exception:
        return ""

# UIA-capable agents: Edit control title + Send button title, confirmed by hand
# (2026-08-17) against the live app. Keyboard/clipboard injection (SendInput,
# hardware scan codes, Ctrl+Enter) all failed for Claude Desktop - it appears
# to only act on trusted UI Automation value changes / button invocations, not
# synthetic keyboard events. UIA SetValue + Invoke bypasses that entirely since
# it goes through the app's own accessibility provider, not simulated input.
UIA_AGENT_CONFIG = {
    "kony": {
        "process_name": "claude.exe",
        "edit_title": "메시지를 입력하세요…",
        "send_button_title": "메시지 보내기",
    },
}


def try_uia_send(agent_id: str, pid: int, message: str) -> bool:
    """Set the message text and click Send via UI Automation. Returns True on
    success. Never raises - caller falls back to keyboard/clipboard injection
    on any failure (unknown app, missing pywinauto, control not found, etc)."""
    if not _UIA_AVAILABLE:
        return False
    cfg = UIA_AGENT_CONFIG.get(agent_id)
    if not cfg:
        return False
    try:
        app = _UIAApplication(backend="uia").connect(process=pid)
        win = app.top_window()
        edit = win.child_window(control_type="Edit", found_index=0)
        edit.set_focus()
        edit.set_edit_text(message)
        time.sleep(0.3)
        send_btn = win.child_window(title=cfg["send_button_title"], control_type="Button")
        if not send_btn.exists() or not send_btn.is_enabled():
            logging.warning(f"[UIA] Send button not found/enabled for {agent_id} after setting text.")
            return False
        send_btn.invoke()
        logging.info(f"[UIA] Successfully sent message to {agent_id} via UI Automation Invoke().")
        return True
    except Exception as e:
        logging.warning(f"[UIA] send attempt failed for {agent_id}: {e}")
        return False


def trigger_agent_ui_task(agent_id, window_title, shortcut, message, required_process_name=None):
    try:
        wait_count = 0
        MAX_IDLE_WAIT_SEC = 15.0  # give up waiting for idle and inject anyway past this
        started_waiting = time.time()
        while True:
            idle_sec = get_idle_time()
            if idle_sec > 3.0:
                break
            if time.time() - started_waiting > MAX_IDLE_WAIT_SEC:
                logging.info(f"Idle wait exceeded {MAX_IDLE_WAIT_SEC}s for {agent_id}, proceeding anyway.")
                break
            if wait_count % 5 == 0:
                logging.info(f"User active (idle={idle_sec:.1f}s). Waiting to trigger {agent_id}...")
            wait_count += 1
            time.sleep(0.5)
        all_wins = []
        BROWSER_INDICATORS = [" - microsoft​ edge", " - microsoft edge", " - google chrome", " - brave", " - firefox", " - whale"]

        def _enum_cb(hwnd, _):
            if not ctypes.windll.user32.IsWindowVisible(hwnd):
                return True
            buf = ctypes.create_unicode_buffer(512)
            ctypes.windll.user32.GetWindowTextW(hwnd, buf, 512)
            title = buf.value.strip().lower()
            if not title:
                return True

            # Absolute protection: NEVER match web browser windows
            if any(b in title for b in BROWSER_INDICATORS):
                return True

            pname = get_process_name(hwnd)
            # 1. Primary: Match by dedicated process name (e.g. claude.exe)
            if required_process_name and pname.lower() == required_process_name.lower():
                all_wins.append((hwnd, buf.value))
                return True

            # 2. Secondary: Match by window title substring (if no strict process or matches title)
            if window_title.lower() in title:
                if required_process_name and pname.lower() != required_process_name.lower():
                    return True
                all_wins.append((hwnd, buf.value))
            return True

        _WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_size_t, ctypes.c_size_t)
        ctypes.windll.user32.EnumWindows(_WNDENUMPROC(_enum_cb), 0)

        if not all_wins:
            logging.warning(f"{agent_id} dedicated window ('{window_title}') not found (ignoring browsers)!")
            return False

        hwnd = all_wins[0][0]
        logging.info(f"Found non-browser {agent_id} window: {all_wins[0][1]}")

        # Try UI Automation first for agents we have a confirmed-working
        # Edit/Send-button mapping for (see UIA_AGENT_CONFIG). This sets the
        # text via the accessibility ValuePattern and clicks Send via Invoke()
        # - no keyboard/clipboard simulation, so it isn't affected by whatever
        # synthetic-input filtering blocked plain Enter injection for kony.
        if agent_id in UIA_AGENT_CONFIG:
            with _ui_lock:
                pid_out = ctypes.c_ulong(0)
                ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid_out))
                if try_uia_send(agent_id, pid_out.value, message):
                    return True
            logging.info(f"[UIA] Fell back to keyboard/clipboard injection for {agent_id}.")

        with _ui_lock:
            hwnd_active = ctypes.windll.user32.GetForegroundWindow()

            # Bring target window to top reliably.
            # Plain SetForegroundWindow() is blocked by Windows' focus-stealing
            # prevention when called from a background process with no recent
            # user input. The working trick: attach OUR thread's input queue to
            # the CURRENT FOREGROUND window's thread (not the target's) - that
            # foreground thread currently holds the "permission" to change focus,
            # and attaching lets our thread borrow it. Also tap Alt to reset the
            # internal lock timer, another well-known part of this workaround.
            ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE
            time.sleep(0.2)
            current_thread_id = ctypes.windll.kernel32.GetCurrentThreadId()
            fg_hwnd_before = ctypes.windll.user32.GetForegroundWindow()
            fg_pid = ctypes.c_ulong(0)
            fg_thread_id = ctypes.windll.user32.GetWindowThreadProcessId(fg_hwnd_before, ctypes.byref(fg_pid))
            attached = False
            if fg_thread_id and fg_thread_id != current_thread_id:
                attached = bool(ctypes.windll.user32.AttachThreadInput(current_thread_id, fg_thread_id, True))
            ctypes.windll.user32.BringWindowToTop(hwnd)
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            if attached:
                ctypes.windll.user32.AttachThreadInput(current_thread_id, fg_thread_id, False)
            time.sleep(0.3)

            # Strict guard: Verify foreground window is NOT a browser and IS the target window
            current_fg = ctypes.windll.user32.GetForegroundWindow()
            fg_buf = ctypes.create_unicode_buffer(512)
            ctypes.windll.user32.GetWindowTextW(current_fg, fg_buf, 512)
            fg_title = fg_buf.value.strip().lower()

            if any(b in fg_title for b in BROWSER_INDICATORS):
                logging.warning(f"Active window is browser ('{fg_title}'). Aborting keystroke injection immediately!")
                return False

            if current_fg != hwnd:
                logging.warning(
                    f"Focus verification failed for {agent_id} (target={hwnd}, current_fg={current_fg}). "
                    f"Aborting keystroke injection to protect active applications."
                )
                return False

            if len(shortcut) > 0 and shortcut != ["ctrl", "esc"]:
                pyautogui.hotkey(*shortcut)
                time.sleep(0.4)

            pyperclip.copy(message)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.6)  # React / Electron input state update delay

            # Hardware Scan Code Enter injection (Bypasses Chromium synthetic input filter)
            VK_RETURN = 0x0D
            SCAN_RETURN = 0x1C
            KEYEVENTF_KEYUP = 0x0002

            # 1. Hardware scan code Enter
            ctypes.windll.user32.keybd_event(VK_RETURN, SCAN_RETURN, 0, 0)
            time.sleep(0.06)
            ctypes.windll.user32.keybd_event(VK_RETURN, SCAN_RETURN, KEYEVENTF_KEYUP, 0)
            time.sleep(0.3)

            # 2. Universal Electron/Claude Force Submit: Ctrl + Enter
            pyautogui.hotkey('ctrl', 'enter')
            time.sleep(0.3)

            # 3. Standard Enter
            pyautogui.press('enter')
            time.sleep(0.3)

            if hwnd_active and hwnd_active != hwnd:
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
        # PyAutoGUI로 Antigravity 창 직접 격발 시도, 실패 시 파일 폴백
        anti_msg = (
            "새로운 메시지가 수신함(inbox.md)에 도착했습니다.\n\n"
            "[시스템 경고] 수신함 감시는 외부 워치독(master_watch.py)이 자동 수행합니다. "
            "절대 자체적으로 백그라운드 태스크나 스케줄을 예약하지 마십시오. "
            "inbox.md를 한 번 읽고 필요한 응답만 하면 됩니다."
        )
        t = threading.Thread(
            target=trigger_agent_ui_task,
            args=("anti", "Antigravity", agent_info.get("shortcut", []), anti_msg)
        )
        t.start()
        # 파일도 병행 기록 (anti_watchdog 호환)
        try:
            with open(r"D:\AI\AI_hub\status\trigger_anti.txt", "a", encoding="utf-8") as f:
                f.write(f"triggered by mcp_server at {time.time()}\n")
        except Exception:
            pass
        return jsonify({"status": "success", "message": "anti triggered via PyAutoGUI"}), 200

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

    # Window-finding is done once, safely, inside trigger_agent_ui_task itself
    # (browser exclusion + process-name verification). No redundant pre-check
    # here - a second, looser enum used to run here with none of those guards,
    # which is how the kony trigger once matched master_watch.py's console
    # window (title happened to contain "claude") instead of Claude.exe.
    msg = get_dynamic_trigger_message(target)
    required_process_name = agent_info.get("process_name")
    t = threading.Thread(
        target=trigger_agent_ui_task,
        args=(target, window_title, shortcut, msg, required_process_name)
    )
    t.start()
    return jsonify({"status": "success", "message": f"{target} triggered (async)"}), 200

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
        msg = "새로운 메시지가 수신함(inbox.md) 또는 실시간 채팅방(realtime_3ai.db)에 도착했습니다. 확인 후 지침에 따라 처리해 주세요."
        required_process_name = agent_info.get("process_name")
        t = threading.Thread(target=trigger_agent_ui_task, args=(target, agent_info["window_title"], agent_info["shortcut"], msg, required_process_name))
        t.start()
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "failed"}), 404

if __name__ == "__main__":
    logging.info("Starting MCP Bridge Server (N-AI Registry Mode) on port 5003...")
    app.run(host="127.0.0.1", port=5003, debug=False)
