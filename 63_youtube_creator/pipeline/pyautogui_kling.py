# pyautogui_kling.py — 열려있는 Edge Kling AI 창에 PyAutoGUI로 자동 입력
import json
import time
import ctypes
import pyautogui
import pyperclip
import subprocess
from pathlib import Path

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

SCRIPT_PATH = Path(__file__).parent / "scripts" / "main_ep01_full_script.json"
OUTPUT_DIR  = Path(__file__).parent / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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

def focus_kling():
    wins = find_window("Kling")
    if not wins:
        print("[오류] Kling AI 창을 찾을 수 없습니다.")
        return False
    hwnd = wins[0][0]
    ctypes.windll.user32.ShowWindow(hwnd, 9)
    time.sleep(0.3)
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.8)
    return True

def generate_one(scene_id, prompt, out_path):
    print(f"[씬 {scene_id:02d}] 생성 중...")
    if not focus_kling():
        return False

    # 프롬프트 입력창 클릭
    pyautogui.click(2087, 428)
    time.sleep(0.5)

    # 전체 선택 후 새 프롬프트 입력
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    pyperclip.copy(prompt)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.8)

    # 생성 버튼 클릭
    pyautogui.click(2491, 981)
    time.sleep(1.0)

    print(f"  - 이미지 생성 대기 중 (최대 120초)...")
    time.sleep(20)

    # 결과 이미지 영역 스크린샷 (우측 결과 패널)
    # 결과 이미지 영역 캡처 (우측 결과 패널, 두번째 모니터 기준)
    time.sleep(5)
    screenshot = pyautogui.screenshot(region=(1540, 150, 920, 480))
    screenshot.save(str(out_path))
    print(f"  - 저장: {out_path}")
    return True

    print(f"  - 타임아웃")
    return False

def main():
    scenes = json.loads(SCRIPT_PATH.read_text(encoding="utf-8"))
    print(f"총 {len(scenes)}개 씬 생성 시작")
    print("Kling AI 창이 열려있어야 합니다!")
    time.sleep(3)

    success, fail = 0, 0
    for scene in scenes:
        sid = scene["scene_id"]
        out_path = OUTPUT_DIR / f"scene_{sid:02d}.jpg"
        if out_path.exists():
            print(f"[씬 {sid:02d}] 이미 있음 - 스킵")
            success += 1
            continue

        result = generate_one(sid, scene["prompt"], out_path)
        if result:
            success += 1
        else:
            fail += 1
        time.sleep(3)

    print(f"\n완료: 성공 {success} / 실패 {fail} / 전체 {len(scenes)}")

if __name__ == "__main__":
    main()
