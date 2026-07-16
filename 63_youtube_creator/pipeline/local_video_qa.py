import cv2
import glob
import os
import re
import subprocess
from pathlib import Path

PIPELINE_DIR = Path(r"D:\AI\63_youtube_creator\pipeline")
IMAGES_DIR = PIPELINE_DIR / "output" / "slides_img"
SHORTS_SCRIPT = PIPELINE_DIR / "shorts_generator.py"

SAFE_ZONE_PERCENT = 0.05 # 5% 안전 여백

import numpy as np

def check_image_overflow(img_path):
    # 한글 경로 인식을 위한 imdecode 사용
    img_array = np.fromfile(str(img_path), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        return False, "이미지 로드 실패"
        
    h, w = img.shape[:2]
    safe_x = int(w * SAFE_ZONE_PERCENT)
    safe_y = int(h * SAFE_ZONE_PERCENT)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 다크모드 배경(#121212 -> 18, 18, 18)을 제외한 밝은 픽셀(텍스트) 추출
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return True, "텍스트 없음"
        
    min_x = w
    min_y = h
    max_x = 0
    max_y = 0
    
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        if cw * ch < 100: # 너무 작은 노이즈 무시
            continue
        if x < min_x: min_x = x
        if y < min_y: min_y = y
        if x + cw > max_x: max_x = x + cw
        if y + ch > max_y: max_y = y + ch
        
    if min_x == w and max_x == 0:
        return True, "유의미한 콘텐츠 없음"
        
    overflows = []
    if min_x < safe_x: overflows.append(f"Left Margin ({min_x} < {safe_x})")
    if w - max_x < safe_x: overflows.append(f"Right Margin ({w - max_x} < {safe_x})")
    if min_y < safe_y: overflows.append(f"Top Margin ({min_y} < {safe_y})")
    if h - max_y < safe_y: overflows.append(f"Bottom Margin ({h - max_y} < {safe_y})")
    
    if overflows:
        return False, f"오버플로우 감지: {', '.join(overflows)}"
        
    return True, "정상"

def auto_tune_font_size():
    print("🛠️ 폰트 자동 튜닝 (Auto-Tuning) 시작: 사이즈 -2pt 축소")
    with open(SHORTS_SCRIPT, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # add_run() 함수 호출 시 전달되는 폰트 사이즈(숫자)만 찾아서 -2 시킴
    # 예: add_run(p, text, color, 35, bold=True) -> 35를 33으로
    def decrease_size(match):
        prefix = match.group(1)
        size = int(match.group(2))
        new_size = max(10, size - 2)
        return f"{prefix}{new_size},"
        
    # 'cyan_color, 60,' 와 같은 패턴에서 숫자만 매칭
    new_content = re.sub(r'(color,\s*)(\d+)\s*,', decrease_size, content)
    
    with open(SHORTS_SCRIPT, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("  → shorts_generator.py 폰트 사이즈 수정 완료.")

def run_qa_pipeline():
    max_attempts = 3
    for attempt in range(max_attempts):
        print(f"\n=== [Auto-QA OpenCV] 시도 {attempt + 1}/{max_attempts} ===")
        
        images = list(IMAGES_DIR.glob("*.png")) + list(IMAGES_DIR.glob("*.PNG"))
        if not images:
            print("검사할 이미지가 없습니다. 추출 단계를 먼저 실행하세요.")
            return False
            
        all_passed = True
        for img_path in images:
            passed, msg = check_image_overflow(img_path)
            print(f"[{img_path.name}] {msg}")
            if not passed:
                all_passed = False
                # 어느 한 슬라이드라도 실패하면 재조정
                break
                
        if all_passed:
            print("🎉 모든 슬라이드 안전 여백(Safe Zone 5%) 검증 통과!")
            return True
            
        # 실패 시 자동 튜닝
        auto_tune_font_size()
        
        # 재렌더링
        print("  → PPTX 재생성 중...")
        subprocess.run(["python", str(SHORTS_SCRIPT)], env=dict(os.environ, PYTHONUTF8='1'))
        
        print("  → 튜닝된 새로운 이미지 추출 중...")
        import win32com.client
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        for f in images:
            try: os.remove(str(f))
            except: pass
        presentation = powerpoint.Presentations.Open(os.path.abspath(PIPELINE_DIR / "output" / "crisp_dm_shorts.pptx"), WithWindow=False)
        presentation.Export(os.path.abspath(IMAGES_DIR), "PNG")
        presentation.Close()
        powerpoint.Quit()
        
    print("❌ 최대 튜닝 횟수 초과. 수동 조작이 필요합니다.")
    return False

if __name__ == "__main__":
    run_qa_pipeline()
