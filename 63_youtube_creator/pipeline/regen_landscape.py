# regen_landscape.py — 가로형 1920x1080으로 씬 이미지 재생성
import sys, json, time, urllib.request, urllib.parse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

OUTPUT_DIR = Path(__file__).parent / "images"
SCRIPT_PATH = Path(__file__).parent / "scripts" / "main_ep01_full_script.json"

scenes = json.loads(SCRIPT_PATH.read_text(encoding='utf-8'))
print(f"가로형 1920x1080으로 {len(scenes)}개 재생성 시작")

success, fail = 0, 0
for scene in scenes:
    sid = scene['scene_id']
    out_path = OUTPUT_DIR / f"scene_{sid:02d}.jpg"

    # 씬 31은 Pillow로 직접 만든 가로형 유지
    if sid == 31:
        print(f"[씬 31] 유지 (Pillow 가로형)")
        success += 1
        continue

    prompt = scene['prompt']
    print(f"[씬 {sid:02d}/{len(scenes)}] 생성 중... ", end="", flush=True)
    try:
        encoded = urllib.parse.quote(prompt)
        url = (
            f"https://image.pollinations.ai/prompt/{encoded}"
            f"?width=1920&height=1080&model=flux&seed={sid*7}&nologo=true"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        if len(data) < 5000:
            raise ValueError(f"응답 크기 너무 작음: {len(data)}")
        out_path.write_bytes(data)
        print(f"완료 ({len(data)//1024}KB)")
        success += 1
    except Exception as e:
        print(f"실패: {e}")
        fail += 1

    time.sleep(3)

print(f"\n완료: 성공 {success} / 실패 {fail} / 전체 {len(scenes)}")
