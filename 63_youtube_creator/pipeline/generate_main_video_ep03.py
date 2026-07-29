"""
EP.03 모듈형 부분 렌더링 파이프라인 (Modular Partial Render Engine v0.3)
- 변경된 Scene만 선택적으로 부분 렌더링 (Partial Re-render)
- 미변경 Scene은 기존 씬 클립(.mp4) 즉시 재사용
- ffmpeg concat 또는 MoviePy로 초고속 전체 병합
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
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, VideoFileClip

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
        print(f"  - ⚡ [씬 클립 재사용] Scene {s_id_padded} 기존 렌더링 완료본 사용: {target_clip_path}")
        return True
        
    print(f"  - 🎬 [씬 부분 렌더링] Scene {s_id_padded} 새 비디오 생성 중...")
    
    # 1. 오디오 생성
    if force_rerender or not os.path.exists(audio_path) or not os.path.exists(timing_path):
        asyncio.run(generate_tts_edge(tts_text, audio_path, timing_path))
        
    # 2. 클립 구성 및 내보내기
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

def build_modular_pipeline(target_scenes_to_rerender=None):
    """모듈형 비디오 병합 파이프라인"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        scenes = json.load(f)
        
    print("==================================================")
    print(f"🚀 [모듈형 부분 렌더링 엔진 v0.3] 총 {len(scenes)}개 씬 점검 시작")
    print("==================================================")
    
    scene_clips = []
    for scene in scenes:
        s_id = scene["scene_id"]
        s_id_padded = f"{int(s_id):02d}"
        scene_clip_path = os.path.join(OUTPUT_DIR, f"scene_{s_id_padded}_clip.mp4")
        
        force_rerender = False
        if target_scenes_to_rerender and s_id in target_scenes_to_rerender:
            force_rerender = True
            
        render_single_scene(scene, scene_clip_path, force_rerender=force_rerender)
        scene_clips.append(VideoFileClip(scene_clip_path))
        
    print("\n==================================================")
    print("🎥 모듈별 씬 클립 고속 병합 진행 중...")
    print("==================================================")
    final_clip = concatenate_videoclips(scene_clips, method="compose")
    final_clip.write_videofile(FINAL_VIDEO, fps=24, codec="libx264", audio_codec="aac", threads=4)
    print(f"\n🎉 [대성공] 모듈형 렌더링 완료! -> {FINAL_VIDEO}")

if __name__ == "__main__":
    # 수정이 필요한 씬 번호만 타겟팅 (예: Scene 2, Scene 6 등) 하거나 None이면 전체 점검
    target_rerender = [2, 6] if len(sys.argv) > 1 and sys.argv[1] == "--partial" else None
    build_modular_pipeline(target_scenes_to_rerender=target_rerender)
