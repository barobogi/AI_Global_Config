# render_three.py – 오늘 3개 에피소드 영상 생성

import sys
import os
# Ensure pipeline package imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main
from scripts.all_episodes import EPISODES

# 선택할 에피소드 키 (예: EP01, EP02, EP03)
selected_keys = ["EP01", "EP02", "EP03"]

for key in selected_keys:
    epi = EPISODES.get(key)
    if not epi:
        print(f"[WARN] {key} not found in EPISODES")
        continue
    script_text = epi["script"]
    output_file = epi["filename"]
    print(f"\n=== Rendering {key}: {epi['title']} -> {output_file} ===")
    try:
        main(script_text, output_file)
        print(f"[DONE] {output_file} generated")
    except Exception as e:
        print(f"[ERROR] Failed to render {output_file}: {e}")
