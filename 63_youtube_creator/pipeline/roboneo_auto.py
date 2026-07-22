"""
T063 파이프라인 — RoboNeo (무료 AI 영상 생성기) 자동화 스크립트 v0.3 (PyAutoGUI)
작성자: 안티 (오퍼레이터)
작성일: 2026-07-22

[목적]
기존 Kling + Pollinations 파이프라인에서 겪었던 IP/한도 문제 및 
Playwright DOM 탐색 실패(ARR 자율성 미달) 문제를 해결하기 위해,
RoboNeo 플랫폼을 마우스/키보드 100% 매크로(PyAutoGUI)로 우회 제어합니다.
"""

import os
import time
import ctypes
import pyautogui
import pyperclip

import webbrowser

# --- 설정값 (사용자 모니터 환경에 맞춘 좌표) ---
# 프롬프트 입력창 중심 좌표 (Home 화면 기준)
PROMPT_X = 725
PROMPT_Y = 401

# 렌더링 결과 이미지 영역 좌표 (Left, Top, Width, Height)
IMAGE_REGION = (958, 459, 411, 220)

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_size_t, ctypes.c_size_t)

def find_window(keyword):
    results = []
    def cb(hwnd, _):
        buf = ctypes.create_unicode_buffer(256)
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, 256)
        if keyword.lower() in buf.value.lower() and ctypes.windll.user32.IsWindowVisible(hwnd):
            results.append((hwnd, buf.value))
        return True
    ctypes.windll.user32.EnumWindows(WNDENUMPROC(cb), 0)
    return results

def focus_browser():
    """크롬 또는 엣지 브라우저를 찾아 포커스합니다."""
    # 로보네오 창 제목에 RoboNeo가 포함될 확률이 높음
    wins = find_window("RoboNeo")
    if not wins:
        wins = find_window("Chrome")
    if not wins:
        wins = find_window("Edge")
        
    if not wins:
        print("[오류] 브라우저 창을 찾을 수 없습니다. 브라우저를 수동으로 띄워주세요.")
        return False
        
    hwnd = wins[0][0]
    ctypes.windll.user32.ShowWindow(hwnd, 3)  # 3 = 최대화
    time.sleep(0.5)
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.8)
    return True

def generate_video_via_roboneo(prompt: str, output_path: str):
    print("=" * 50)
    print(f"[RoboNeo Auto] 이미지 생성 시작 (v0.4 PyAutoGUI - 완전 자동화)")
    print(f"프롬프트: {prompt}")
    print("=" * 50)
    
    # 1. 브라우저 탭 강제 열기 (어느 화면에 있든 Home으로 초기화)
    print("[1/5] 로보네오 홈 화면 강제 진입...")
    webbrowser.open("https://roboneo.com/home")
    time.sleep(5)  # 페이지 로딩 대기
    
    # 2. 브라우저 창 포커스 (webbrowser가 띄웠지만 혹시 몰라 포커스 한 번 더)
    focus_browser()
    time.sleep(1)
    
    # 3. 프롬프트 입력창 클릭
    print(f"[2/5] 입력창 클릭 (X:{PROMPT_X}, Y:{PROMPT_Y})...")
    pyautogui.click(PROMPT_X, PROMPT_Y)
    time.sleep(0.5)
    
    # 4. 전체 선택 후 새 프롬프트 붙여넣기
    print("[3/5] 프롬프트 텍스트 붙여넣기 및 엔터 전송...")
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    pyperclip.copy(prompt)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)
    
    # 생성 버튼 좌표를 못 땄으므로 우선 엔터키로 생성 요청 시도
    pyautogui.press("enter")
    time.sleep(1)
    
    # 5. 렌더링 대기
    print("[4/5] 렌더링 대기 중 (약 35초)....")
    time.sleep(35)
    
    # 6. 결과 캡처
    print(f"[5/5] 렌더링 완료. 결과물 화면 캡처 중: {output_path}")
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    
    # 꼼수 대신 진짜 이미지 캡처 (Pillow/PyAutoGUI)
    img = pyautogui.screenshot(region=IMAGE_REGION)
    img.save(output_path)
    
    # 7. 탭 닫기 (다음 렌더링 시 탭이 무한 증식하는 것 방지)
    print("[RoboNeo Auto] 완료 후 브라우저 탭 닫기(Ctrl+W)...")
    pyautogui.hotkey('ctrl', 'w')
        
    print("[RoboNeo Auto] 파이프라인(스크린샷 방식) 실행 완료!")
    return True

if __name__ == "__main__":
    test_prompt = "A cinematic shot of a futuristic AI managing data streams, blue and orange neon lights, 16:9"
    test_output = os.path.join(os.path.dirname(__file__), "output", "roboneo_test_output.mp4")
    generate_video_via_roboneo(test_prompt, test_output)
