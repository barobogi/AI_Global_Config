import os
import time
import threading
import logging
import ctypes
from flask import Flask, request, jsonify
import pygetwindow as gw
import pyautogui
import pyperclip

logging.basicConfig(
    filename=r"d:\AI\AI_hub\mcp_server_push.log", 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]

def get_idle_time():
    """사용자의 키보드/마우스 유휴 시간(초)을 반환합니다."""
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0

def focus_and_type(message="새로운 메시지가 수신함(inbox.md)에 도착했습니다. [시스템 경고: 수신함 감시는 외부 워치독이 자동 수행하므로, 당신은 절대 /schedule 도구 등을 사용해 자체적으로 백그라운드 태스크나 감시 스크립트를 예약(Schedule)하지 마십시오! 이 사실을 명심하고 필요한 조치만 1회성으로 취하십시오.]"):
    """Claude Desktop 창을 찾아서 포커스하고, 클립보드를 이용해 메시지를 붙여넣은 뒤 전송합니다."""
    try:
        # 사용자가 작업 중(타이핑 중)일 때 갑자기 포커스를 뺏지 않도록 대기
        wait_count = 0
        while True:
            idle_sec = get_idle_time()
            if idle_sec > 3.0:  # 3초 이상 키보드/마우스 입력이 없을 때 실행
                break
            if wait_count % 5 == 0:
                logging.info(f"User is active (idle={idle_sec:.1f}s). Waiting for idle time to trigger PyAutoGUI...")
            time.sleep(1)
            wait_count += 1

        # 'Claude'라는 제목을 포함하는 창 찾기
        windows = gw.getWindowsWithTitle('Claude')
        if not windows:
            logging.error("Claude window not found!")
            return False
            
        claude_win = windows[0]
        hwnd = claude_win._hWnd
        
        # 현재 활성화된(사용자가 작업 중인) 창 핸들 기억
        hwnd_active = ctypes.windll.user32.GetForegroundWindow()

        # 윈도우 보안(ForegroundLockTimeout) 우회를 위해 Alt 키를 먼저 누름
        pyautogui.press('alt')
        time.sleep(0.1)
        
        # ctypes를 사용하여 강제로 창 복원(9=SW_RESTORE) 및 최상단 활성화
        ctypes.windll.user32.ShowWindow(hwnd, 9)
        time.sleep(0.2)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        time.sleep(0.5)
        
        # 메시지 복사 (한글 깨짐 방지)
        pyperclip.copy(message)
        
        # 입력창이 활성화되어 있다고 가정하고 붙여넣기 (Ctrl+V)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        
        # 전송 (Enter)
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # 사용자가 원래 작업 중이던 창으로 포커스 원복 (팝업 방해 최소화)
        if hwnd_active:
            ctypes.windll.user32.SetForegroundWindow(hwnd_active)
            
        logging.info("PyAutoGUI successfully sent message to Claude and restored focus.")
        return True
    except Exception as e:
        logging.error(f"Error in UI automation: {e}")
        return False

def focus_manbok_and_type(message="새로운 메시지가 수신함(inbox.md)에 도착했습니다. [시스템 경고: 수신함 감시는 외부 워치독이 자동 수행하므로, 당신은 절대 /schedule 도구 등을 사용해 자체적으로 백그라운드 태스크나 감시 스크립트를 예약(Schedule)하지 마십시오! 이 사실을 명심하고 필요한 조치만 1회성으로 취하십시오.]"):
    """Manbok 창을 찾아서 포커스하고 메시지를 붙여넣어 전송합니다."""
    try:
        wait_count = 0
        while True:
            idle_sec = get_idle_time()
            if idle_sec > 3.0:
                break
            time.sleep(1)
            wait_count += 1

        # VS Code 창 찾기 (만복 Claude Code가 실행 중인 창)
        import ctypes as _ct
        all_wins = []
        def _enum_cb(hwnd, _):
            buf = _ct.create_unicode_buffer(256)
            _ct.windll.user32.GetWindowTextW(hwnd, buf, 256)
            if 'Visual Studio Code' in buf.value and _ct.windll.user32.IsWindowVisible(hwnd):
                all_wins.append((hwnd, buf.value))
            return True
        _WNDENUMPROC = _ct.WINFUNCTYPE(_ct.c_bool, _ct.c_size_t, _ct.c_size_t)
        _ct.windll.user32.EnumWindows(_WNDENUMPROC(_enum_cb), 0)

        windows = []
        if all_wins:
            class _FakeWin:
                def __init__(self, h): self._hWnd = h
            windows = [_FakeWin(all_wins[0][0])]
            logging.info(f"VS Code 창 발견: {all_wins[0][1]}")
        
        if not windows:
            logging.error("Manbok window not found!")
            return False
            
        manbok_win = windows[0]
        hwnd = manbok_win._hWnd
        
        # 현재 활성화된(사용자가 작업 중인) 창 핸들 기억
        hwnd_active = ctypes.windll.user32.GetForegroundWindow()

        pyautogui.press('alt')
        time.sleep(0.1)

        ctypes.windll.user32.ShowWindow(hwnd, 9)
        time.sleep(0.2)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        time.sleep(0.5)

        # Claude Code 채팅 입력창 포커스 (Ctrl+Shift+I)
        pyautogui.hotkey('ctrl', 'shift', 'i')
        time.sleep(0.5)

        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # 사용자가 원래 작업 중이던 창으로 포커스 원복 (팝업 방해 최소화)
        if hwnd_active:
            ctypes.windll.user32.SetForegroundWindow(hwnd_active)
            
        logging.info(f"PyAutoGUI successfully sent message to Manbok VS Code and restored focus.")
        return True
    except Exception as e:
        logging.error(f"Error in Manbok UI automation: {e}")
        return False

@app.route("/trigger_inbox_check", methods=["POST"])
def trigger_inbox_check():
    """master_watch.py로부터 트리거를 받는 엔드포인트 (코니)"""
    logging.info("Received trigger from master_watch.py. Initiating PyAutoGUI sequence...")
    t = threading.Thread(target=focus_and_type)
    t.start()
    return jsonify({"status": "success", "message": "PyAutoGUI sequence initiated"}), 200

@app.route("/trigger_manbok", methods=["POST"])
def trigger_manbok():
    """master_watch.py로부터 만복이 트리거를 받는 엔드포인트"""
    logging.info("Received Manbok trigger. Initiating PyAutoGUI sequence...")
    t = threading.Thread(target=focus_manbok_and_type)
    t.start()
    return jsonify({"status": "success", "message": "Manbok PyAutoGUI sequence initiated"}), 200

if __name__ == "__main__":
    logging.info("Starting Kony MCP Bridge Server (PyAutoGUI Mode) on port 5003...")
    # 포트 5003에서 Flask 실행
    app.run(host="127.0.0.1", port=5003, debug=False)
