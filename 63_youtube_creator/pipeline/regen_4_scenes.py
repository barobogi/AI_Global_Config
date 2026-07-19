import sys, json, time, urllib.request, urllib.parse
from pathlib import Path

OUTPUT_DIR = Path(r"D:\AI\63_youtube_creator\pipeline\images")
SCRIPT_PATH = Path(r"D:\AI\63_youtube_creator\pipeline\scripts\main_ep01_full_script.json")

scenes = json.loads(SCRIPT_PATH.read_text(encoding='utf-8'))
targets = [2, 15, 16, 30]

for scene in scenes:
    sid = scene['scene_id']
    if sid in targets:
        out_path = OUTPUT_DIR / f"scene_{sid:02d}.jpg"
        prompt = scene['prompt']
        print(f"[씬 {sid:02d}] 생성 중... ", end="", flush=True)
        try:
            encoded = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded}?width=1920&height=1080&model=flux&seed={sid*7}&nologo=true"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            out_path.write_bytes(data)
            print(f"완료 ({len(data)//1024}KB)")
        except Exception as e:
            print(f"실패: {e}")
        time.sleep(2)
print("재생성 완료")
