import os
import json
import asyncio
import subprocess
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

try:
    from kling_auto import generate_scene_image
except ImportError:
    from byteplus_auto import generate_scene_image

SCRIPT_FILE = r"D:\AI\63_youtube_creator\pipeline\scripts\main_ep01_full_script.json"
OUTPUT_DIR = r"D:\AI\63_youtube_creator\pipeline\output\ep01"
FINAL_VIDEO = r"D:\AI\63_youtube_creator\pipeline\output\Main_EP01_AI_Governance.mp4"

async def generate_tts_edge(text: str, output_path: str):
    """edge-tts를 사용하여 한국어 음성 생성 (서브프로세스 호출)"""
    print(f"  - TTS 생성 중: {output_path}")
    # edge-tts 보이스 설정 (ko-KR-SunHiNeural 등)
    cmd = [
        "edge-tts",
        "--voice", "ko-KR-SunHiNeural",
        "--text", text,
        "--write-media", output_path
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"TTS 생성 실패 (edge-tts가 설치되어 있어야 합니다): {e}")
        return False

async def build_pipeline():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        scenes = json.load(f)
        
    # 씬 31은 main_ep01_full_script.json에 이미 포함됨 — 중복 append 제거
        
    print(f"총 {len(scenes)}개의 장면(Scene) 렌더링 파이프라인 시작...\n")
    
    clips = []
    
    # 1. 에셋(이미지, 오디오) 생성
    for scene in scenes:
        s_id = scene["scene_id"]
        text = scene["text"]
        prompt = scene["prompt"]
        
        s_id_padded = f"{int(s_id):02d}"
        print(f"=== Scene {s_id_padded} 처리 중 ===")
        
        img_path = rf"D:\AI\63_youtube_creator\pipeline\images\scene_{s_id_padded}.jpg"
        audio_path = os.path.join(OUTPUT_DIR, f"scene_{s_id_padded}.mp3")
        
        if not os.path.exists(img_path):
            print(f"Scene {s_id_padded} 이미지를 찾을 수 없습니다: {img_path}. 파이프라인 중단.")
            return
        else:
            print(f"  - 만복이 생성 이미지 로드 성공: {img_path}")
            
        # 오디오 생성
        if not os.path.exists(audio_path):
            await generate_tts_edge(text, audio_path)
        else:
            print(f"  - 오디오 캐시 사용: {audio_path}")
            
        # 2. MoviePy 클립 생성 및 조립
        try:
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration + 0.5 # 음성 길이 + 0.5초 여유
            
            # 이미지 클립 — 1920×1080으로 리사이즈 (Pollinations 실제 해상도 무관)
            from PIL import Image as PILImage
            import numpy as np
            pil_img = PILImage.open(img_path).resize((1920, 1080), PILImage.LANCZOS)
            img_array = np.array(pil_img)
            img_clip = ImageClip(img_array).with_duration(duration)
            W, H = 1920, 1080

            # 자막 텍스트 줄바꿈 (한글 기준 1줄 35자)
            import textwrap
            wrapped_text = "\n".join(textwrap.wrap(text, width=35)) + "\n "

            # 자막 생성 — 이미지 높이 기준 동적 위치
            font_size = int(H * 0.055)  # 높이의 5.5% (약 60px)
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
            # 텍스트 클립의 실제 높이를 반영하여 하단 여백 60px 확보
            subtitle_y = H - txt_clip.size[1] - 60
            txt_clip = txt_clip.with_position(('center', subtitle_y)).with_duration(duration)
            
            # 이미지 위에 자막 합성
            video = CompositeVideoClip([img_clip, txt_clip])
            
            # 오디오 합성
            video = video.with_audio(audio_clip)
            
            clips.append(video)
        except Exception as e:
            print(f"Scene {s_id} 비디오 클립 생성 중 오류: {e}")
            return
            
    # 3. 전체 클립 이어붙이기 및 최종 렌더링
    if clips:
        print("\n=== 최종 비디오 렌더링 중 ===")
        final_clip = concatenate_videoclips(clips, method="compose")
        # 초당 24프레임으로 렌더링 (빠른 렌더링을 위해 스레드 사용)
        final_clip.write_videofile(FINAL_VIDEO, fps=24, codec="libx264", audio_codec="aac", threads=4)
        print(f"\n[대성공] 본편 1부 렌더링 완벽 완료! -> {FINAL_VIDEO}")

if __name__ == "__main__":
    asyncio.run(build_pipeline())
