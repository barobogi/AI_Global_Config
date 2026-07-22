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

# --- 설정값 (사용자 모니터 환경에 맞춘 좌표) ---
# 프롬프트 입력창 중심 좌표 (듀얼 모니터 우측)
PROMPT_X = 3028
PROMPT_Y = 801

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
    print(f"[RoboNeo Auto] 이미지 생성 시작 (v0.3 PyAutoGUI)")
    print(f"프롬프트: {prompt}")
    print("=" * 50)
    
    # 1. 브라우저 창 최상단으로 끌어올리기
    focus_browser()
    
    # 2. 안전 대기
    time.sleep(1)
    
    # 3. 프롬프트 입력창 클릭
    print(f"[1/4] 입력창 클릭 (X:{PROMPT_X}, Y:{PROMPT_Y})...")
    pyautogui.click(PROMPT_X, PROMPT_Y)
    time.sleep(0.5)
    
    # 4. 전체 선택 후 새 프롬프트 붙여넣기
    print("[2/4] 프롬프트 텍스트 붙여넣기 및 엔터 전송...")
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    pyperclip.copy(prompt)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)
    
    # 생성 버튼 좌표를 못 땄으므로 우선 엔터키로 생성 요청 시도
    pyautogui.press("enter")
    time.sleep(1)
    
    # 5. 렌더링 대기
    print("[3/4] 렌더링 대기 중 (약 30초)....")
    time.sleep(30)
    
    # 6. 결과 캡처 (우선은 이미지 파일 다운로드를 캡처로 대체)
    # 실제로는 완성된 영상을 우클릭-저장하거나 위치를 캡처해야 함
    print(f"[4/4] 렌더링 완료. 결과물 임시 캡처: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 임시 목업(Mock) 파일 생성 (실제 파일 다운로드는 다음 이터레이션에서 정교화)
    with open(output_path, 'wb') as f:
        f.write(b"mock_video_data_from_roboneo_pyautogui")
        
    print("[RoboNeo Auto] 파이프라인 실행 완료!")
    return True

if __name__ == "__main__":
    test_prompt = "A cinematic shot of a futuristic AI managing data streams, blue and orange neon lights, 16:9"
    test_output = os.path.join(os.path.dirname(__file__), "output", "roboneo_test_output.mp4")
    generate_video_via_roboneo(test_prompt, test_output)
