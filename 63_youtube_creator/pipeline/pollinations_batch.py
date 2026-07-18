# pollinations_batch.py — Pollinations.ai로 30개 씬 이미지 배치 생성
import sys, json, time, urllib.request, urllib.parse
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SCRIPT_PATH = Path(__file__).parent / "scripts" / "main_ep01_full_script.json"
OUTPUT_DIR  = Path(__file__).parent / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate(prompt, out_path, seed=42):
    encoded = urllib.parse.quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width=1080&height=1920&model=flux&seed={seed}&nologo=true&enhance=true"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    if len(data) < 5000:
        raise ValueError(f"응답 크기 너무 작음: {len(data)} bytes")
    Path(out_path).write_bytes(data)
    return True

def main():
    scenes = json.loads(SCRIPT_PATH.read_text(encoding="utf-8"))
    total = len(scenes)
    print(f"Pollinations.ai 배치 시작 — 총 {total}개")

    success, fail = 0, 0
    for scene in scenes:
        sid = scene["scene_id"]
        prompt = scene["prompt"]
        out_path = OUTPUT_DIR / f"scene_{sid:02d}.jpg"

        if out_path.exists():
            print(f"[씬 {sid:02d}] 스킵 (이미 있음)")
            success += 1
            continue

        print(f"[씬 {sid:02d}/{total}] 생성 중... ", end="", flush=True)
        try:
            generate(prompt, out_path, seed=sid * 7)
            kb = out_path.stat().st_size // 1024
            print(f"완료 ({kb}KB)")
            success += 1
        except Exception as e:
            print(f"실패: {e}")
            fail += 1

        time.sleep(2)

    print(f"\n완료: 성공 {success} / 실패 {fail} / 전체 {total}")
    print(f"저장 위치: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
