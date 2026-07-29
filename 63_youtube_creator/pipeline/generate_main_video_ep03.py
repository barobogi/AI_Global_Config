"""
EP.03 모듈형 순간 병합 파이프라인 (True Zero-Reencoding Modular Engine v0.4)
- 변경된 Scene만 선택적으로 부분 렌더링 (Partial Re-render)
- 미변경 Scene은 기존 씬 클립(.mp4) 재사용
- ffmpeg -f concat (Stream Copy) 모드로 재인코딩 없이 1초 만에 순간 합성!
"""
import os
import json
import asyncio
import subprocess
import sys
import re
import textwrap
import edge_tts
from PIL import Image as PILImage
import numpy as np
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

sys.path.insert(0, os.path.dirname(__file__))
from pollinations_auto import generate_video_via_pollinations
from script_analyzer import validate_and_fix_tts_pronunciation

SCRIPT_FILE = r"D:\AI\63_youtube_creator\pipeline\scripts\main_ep03_full_script.json"
OUTPUT_DIR = r"D:\AI\63_youtube_creator\pipeline\output\ep03"
FINAL_VIDEO = r"D:\AI\63_youtube_creator\pipeline\output\Main_EP03_AI_Remembers_Me.mp4"
IMAGES_DIR = r"D:\AI\63_youtube_creator\pipeline\images\ep03"

if sys.stdout is not None and getattr(sys.stdout, "encoding", None) is not None:
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

async def generate_tts_edge(text: str, output_path: str, timing_path: str):
    print(f"  - Edge-TTS 생성 및 타임스탬프 추출 중: {os.path.basename(output_path)}")
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

def render_single_scene(scene, target_clip_path, force_rerender=False):
    """단일 씬 개별 클립 비디오 렌더링"""
    s_id = scene["scene_id"]
    s_id_padded = f"{int(s_id):02d}"
    
    text = scene["text"]
    raw_tts_text = scene.get("tts_text", text)
    tts_text, is_modified = validate_and_fix_tts_pronunciation(raw_tts_text)
    bg_prompt = scene.get("prompt")
    
    img_path = os.path.join(IMAGES_DIR, f"scene_{s_id_padded}.jpg")
    audio_path = os.path.join(OUTPUT_DIR, f"scene_{s_id_padded}.mp3")
    timing_path = os.path.join(OUTPUT_DIR, f"scene_{s_id_padded}_timing.json")
    
    if os.path.exists(target_clip_path) and not force_rerender:
        print(f"  - ⚡ [씬 클립 재사용] Scene {s_id_padded} 기존 렌더링 완료본 사용: {os.path.basename(target_clip_path)}")
        return True
        
    print(f"  - 🎬 [씬 부분 렌더링] Scene {s_id_padded} 새 비디오 인코딩 중...")
    
    if force_rerender or not os.path.exists(audio_path) or not os.path.exists(timing_path):
        asyncio.run(generate_tts_edge(tts_text, audio_path, timing_path))
        
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    
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
        wrapped_text = "\n".join(textwrap.wrap(sentence.strip(), width=38)) + "\n "
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
        
    scene_video = CompositeVideoClip([img_clip] + txt_clips).with_audio(audio_clip).with_duration(duration)
    scene_video.write_videofile(target_clip_path, fps=24, codec="libx264", audio_codec="aac", threads=4)
    return True

def fast_ffmpeg_concat(clip_paths, output_path):
    """ffmpeg -f concat (Stream Copy) 방식을 사용해 1초 만에 무손실 순간 합성"""
    list_file = os.path.join(OUTPUT_DIR, "concat_list.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for path in clip_paths:
            # ffmpeg concat 파싱용 상대/절대 경로 인코딩
            escaped_path = path.replace("\\", "/")
            f.write(f"file '{escaped_path}'\n")
            
    print(f"🚀 [ffmpeg Stream Copy] 재인코딩 0% 순간 합성 실행 중...")
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", list_file, "-c", "copy", output_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"🎉 [대성공] 1초 만에 무손실 순간 합성 완수! -> {output_path}")
        return True
    else:
        print(f"⚠️ [Warning] ffmpeg Stream Copy 실패 ({res.stderr}), 폴백 진행")
        return False

def build_fast_modular_pipeline(target_scenes_to_rerender=None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        scenes = json.load(f)
        
    print("==================================================")
    print(f"⚡ [True Zero-Reencoding Engine v0.4] 총 {len(scenes)}개 씬 점검")
    print("==================================================")
    
    scene_clip_paths = []
    for scene in scenes:
        s_id = scene["scene_id"]
        s_id_padded = f"{int(s_id):02d}"
        scene_clip_path = os.path.join(OUTPUT_DIR, f"scene_{s_id_padded}_clip.mp4")
        
        force_rerender = False
        if target_scenes_to_rerender and s_id in target_scenes_to_rerender:
            force_rerender = True
            
        render_single_scene(scene, scene_clip_path, force_rerender=force_rerender)
        scene_clip_paths.append(scene_clip_path)
        
    print("\n==================================================")
    print("⚡ 씬 클립 1초 순간 결합 진행 중 (ffmpeg Stream Copy)...")
    print("==================================================")
    fast_ffmpeg_concat(scene_clip_paths, FINAL_VIDEO)

if __name__ == "__main__":
    target_rerender = [2, 6] if len(sys.argv) > 1 and sys.argv[1] == "--partial" else None
    build_fast_modular_pipeline(target_scenes_to_rerender=target_rerender)
