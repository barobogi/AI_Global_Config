import os
import json
import asyncio
import subprocess
import sys
import re
import textwrap
import edge_tts
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

SCRIPT_FILE = r"D:\AI\63_youtube_creator\pipeline\scripts\main_ep02_full_script.json"
OUTPUT_DIR = r"D:\AI\63_youtube_creator\pipeline\output\ep02"
FINAL_VIDEO = r"D:\AI\63_youtube_creator\pipeline\output\Main_EP02_System_Evolution.mp4"
IMAGES_DIR = r"D:\AI\63_youtube_creator\pipeline\images\ep02"

async def generate_tts_edge(text: str, output_path: str, timing_path: str):
    print(f"  - TTS 생성 및 타임스탬프 추출 중: {output_path}")
    communicate = edge_tts.Communicate(text, "ko-KR-SunHiNeural")
    word_boundaries = []
    
    with open(output_path, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "SentenceBoundary":
                start_sec = chunk["offset"] / 10**7
                duration_sec = chunk["duration"] / 10**7
                word_boundaries.append({
                    "text": chunk["text"],
                    "start": start_sec,
                    "end": start_sec + duration_sec
                })
                
    with open(timing_path, "w", encoding="utf-8") as f:
        json.dump(word_boundaries, f, ensure_ascii=False, indent=2)
    return True

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
        timing_path = os.path.join(OUTPUT_DIR, f"scene_{s_id_padded}_timing.json")
        
        if not os.path.exists(img_path):
            error_msg = f"Scene {s_id_padded} 이미지를 찾을 수 없습니다: {img_path}. 파이프라인 중단."
            print(error_msg)
            sys.exit(1)
        else:
            print(f"  - 이미지 로드 성공: {img_path}")
            
        # 기존 오디오 캐시 무효화 (타임스탬프 파일이 없으면 무조건 재생성)
        if not os.path.exists(audio_path) or not os.path.exists(timing_path):
            await generate_tts_edge(tts_text, audio_path, timing_path)
        else:
            print(f"  - 오디오 및 타임스탬프 캐시 사용: {audio_path}")
            
        try:
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
            
            from PIL import Image as PILImage
            import numpy as np
            pil_img = PILImage.open(img_path).resize((1920, 1080), PILImage.LANCZOS)
            img_array = np.array(pil_img)
            img_clip = ImageClip(img_array).with_duration(duration)
            W, H = 1920, 1080

            font_size = int(H * 0.055)
            
            with open(timing_path, "r", encoding="utf-8") as f:
                word_boundaries = json.load(f)
                
            txt_clips = []
            
            for chunk in word_boundaries:
                sentence = chunk["text"]
                start_time = chunk["start"]
                end_time = chunk["end"]
                
                wrapped_text = "\n".join(textwrap.wrap(sentence.strip(), width=35)) + "\n "
                
                # 강제로 오디오 길이를 초과하지 않도록 보정
                if end_time > duration: end_time = duration
                if start_time > duration: start_time = max(0, duration - 1)
                
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
                txt_clip = txt_clip.with_position(('center', subtitle_y)).with_start(start_time).with_end(end_time)
                txt_clips.append(txt_clip)
            
            video = CompositeVideoClip([img_clip] + txt_clips)
            video = video.with_audio(audio_clip).with_duration(duration)
            
            clips.append(video)
        except Exception as e:
            error_msg = f"Scene {s_id} 비디오 클립 생성 중 오류: {e}"
            print(error_msg)
            sys.exit(1)
            
    if clips:
        print("\n=== 최종 비디오 렌더링 중 ===")
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(FINAL_VIDEO, fps=24, codec="libx264", audio_codec="aac", threads=4)
        print(f"\n[대성공] 본편 EP02 렌더링 완벽 완료! -> {FINAL_VIDEO}")
        
        print("\n=== 시각 품질 검증(ToFu/OCR) 시작 ===")
        qa_script = os.path.join(os.path.dirname(__file__), "qa_video_visuals.py")
        try:
            subprocess.run([sys.executable, qa_script, FINAL_VIDEO], check=True)
            print("[검증 통과] 폰트 깨짐 및 오버플로우 없음!")
        except subprocess.CalledProcessError:
            error_msg = "[검증 실패] 폰트 깨짐 또는 오버플로우가 발견되었습니다! (ToFu 에러)"
            print(error_msg)
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(build_pipeline())
