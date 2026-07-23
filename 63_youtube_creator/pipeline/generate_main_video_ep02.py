import os
import json
import asyncio
import subprocess
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

SCRIPT_FILE = r"D:\AI\63_youtube_creator\pipeline\scripts\main_ep02_full_script.json"
OUTPUT_DIR = r"D:\AI\63_youtube_creator\pipeline\output\ep02"
FINAL_VIDEO = r"D:\AI\63_youtube_creator\pipeline\output\Main_EP02_System_Evolution.mp4"
IMAGES_DIR = r"D:\AI\63_youtube_creator\pipeline\images\ep02"

async def generate_tts_edge(text: str, output_path: str):
    print(f"  - TTS 생성 중: {output_path}")
    cmd = [
        "edge-tts",
        "--voice", "ko-KR-SunHiNeural",
        "--text", text,
        "--write-media", output_path
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"TTS 생성 실패: {e.stderr}")
        return False

async def build_pipeline():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        scenes = json.load(f)
        
    print(f"총 {len(scenes)}개의 장면(Scene) 렌더링 파이프라인 시작...\n")
    
    clips = []
    
    for scene in scenes:
        s_id = scene["scene_id"]
        text = scene["text"]
        tts_text = scene.get("tts_text", text)
        
        s_id_padded = f"{int(s_id):02d}"
        print(f"=== Scene {s_id_padded} 처리 중 ===")
        
        img_path = os.path.join(IMAGES_DIR, f"scene_{s_id_padded}.jpg")
        audio_path = os.path.join(OUTPUT_DIR, f"scene_{s_id_padded}.mp3")
        
        if not os.path.exists(img_path):
            print(f"Scene {s_id_padded} 이미지를 찾을 수 없습니다: {img_path}. 파이프라인 중단.")
            return
        else:
            print(f"  - 이미지 로드 성공: {img_path}")
            
        if not os.path.exists(audio_path):
            await generate_tts_edge(tts_text, audio_path)
        else:
            print(f"  - 오디오 캐시 사용: {audio_path}")
            
        try:
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration + 0.5
            
            from PIL import Image as PILImage
            import numpy as np
            pil_img = PILImage.open(img_path).resize((1920, 1080), PILImage.LANCZOS)
            img_array = np.array(pil_img)
            img_clip = ImageClip(img_array).with_duration(duration)
            W, H = 1920, 1080

            import textwrap
            wrapped_text = "\n".join(textwrap.wrap(text, width=35)) + "\n "

            font_size = int(H * 0.055)
            txt_clip = TextClip(
                font=r"C:\Windows\Fonts\malgun.ttf",
                text=wrapped_text,
                font_size=font_size,
                color="white",
                stroke_color="black",
                stroke_width=2,
                method="label",
                text_align="center"
            )
            subtitle_y = H - txt_clip.size[1] - 60
            txt_clip = txt_clip.with_position(('center', subtitle_y)).with_duration(duration)
            
            video = CompositeVideoClip([img_clip, txt_clip])
            video = video.with_audio(audio_clip)
            
            clips.append(video)
        except Exception as e:
            print(f"Scene {s_id} 비디오 클립 생성 중 오류: {e}")
            return
            
    if clips:
        print("\n=== 최종 비디오 렌더링 중 ===")
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(FINAL_VIDEO, fps=24, codec="libx264", audio_codec="aac", threads=4)
        print(f"\n[대성공] 본편 EP02 렌더링 완벽 완료! -> {FINAL_VIDEO}")
        
        print("\n=== 시각 품질 검증(ToFu/OCR) 시작 ===")
        qa_script = os.path.join(os.path.dirname(__file__), "qa_video_visuals.py")
        try:
            subprocess.run([sys.executable, qa_script, FINAL_VIDEO], check=True)
            print("[검증 통과] 폰트 깨짐 없음!")
        except subprocess.CalledProcessError:
            print("[검증 실패] 폰트 깨짐이 발견되었습니다! (ToFu 에러)")
            sys.exit(1)

if __name__ == "__main__":
    import sys
    asyncio.run(build_pipeline())
