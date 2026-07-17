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

def focus_and_type(message="새로운 메시지가 수신함(inbox.md)에 도착했습니다. 확인 후 필요한 조치를 취해주세요."):
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
        logging.info("PyAutoGUI successfully sent message to Claude.")
        return True
    except Exception as e:
        logging.error(f"Error in UI automation: {e}")
        return False

@app.route("/trigger_inbox_check", methods=["POST"])
def trigger_inbox_check():
    """master_watch.py로부터 트리거를 받는 엔드포인트"""
    logging.info("Received trigger from master_watch.py. Initiating PyAutoGUI sequence...")
    
    # 백그라운드 스레드에서 UI 자동화 실행 (HTTP 응답을 블록하지 않기 위해)
    t = threading.Thread(target=focus_and_type)
    t.start()
    
    return jsonify({"status": "success", "message": "PyAutoGUI sequence initiated"}), 200

if __name__ == "__main__":
    logging.info("Starting Kony MCP Bridge Server (PyAutoGUI Mode) on port 5003...")
    # 포트 5003에서 Flask 실행
    app.run(host="127.0.0.1", port=5003, debug=False)
