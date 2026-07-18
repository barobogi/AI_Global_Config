# batch_generate_images.py — 만복이 직접 30개 씬 이미지 생성
import json
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kling_auto import generate_scene_image

SCRIPT_PATH = Path(__file__).parent / "scripts" / "main_ep01_full_script.json"
OUTPUT_DIR  = Path(__file__).parent / "images"

async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scenes = json.loads(SCRIPT_PATH.read_text(encoding="utf-8"))
    total = len(scenes)
    print(f"총 {total}개 씬 이미지 생성 시작")

    success, fail = 0, 0
    for scene in scenes:
        sid = scene["scene_id"]
        prompt = scene["prompt"]
        out_path = str(OUTPUT_DIR / f"scene_{sid:02d}.jpg")

        if Path(out_path).exists():
            print(f"[씬 {sid:02d}] 이미 있음 — 스킵")
            success += 1
            continue

        print(f"\n[씬 {sid:02d}/{total}] 생성 중...")
        result = await generate_scene_image(prompt, out_path)
        if result:
            success += 1
            print(f"[씬 {sid:02d}] OK 완료 ({success}/{total})")
        else:
            fail += 1
            print(f"[씬 {sid:02d}] FAIL 실패 (누적 실패: {fail})")

        # 요청 간격 5초 (rate limit 방지)
        await asyncio.sleep(5)

    print(f"\n===== 완료 =====")
    print(f"성공: {success} / 실패: {fail} / 전체: {total}")

if __name__ == "__main__":
    asyncio.run(main())
