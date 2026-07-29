"""
EP.03 본편 파이프라인 렌더러 — AI가 나를 기억하기 시작했다 (TTS 3AI -> 쓰리에이아이 교정 및 자동 하드닝 훅 내장)
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
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

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

async def build_pipeline(force_clean_tts=False):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    if force_clean_tts:
        for f in os.listdir(OUTPUT_DIR):
            if f.endswith(".mp3") or f.endswith("_timing.json"):
                try:
                    os.remove(os.path.join(OUTPUT_DIR, f))
                except Exception:
                    pass
        print("🧹 [TTS 캐시 초기화] '3AI' -> '쓰리에이아이' 낭독 교정을 위해 오디오 캐시를 초기화했습니다.")

    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        scenes = json.load(f)
        
    print(f"==================================================")
    print(f"🎬 [EP.03] 본편 렌더링 파이프라인 엔진 시작 (총 {len(scenes)}개 씬)")
    print(f"==================================================\n")
    
    clips = []
    
    for scene in scenes:
        s_id = scene["scene_id"]
        text = scene["text"]
        raw_tts_text = scene.get("tts_text", text)
        
        # [자동 하드닝 훅] 3AI -> 쓰리에이아이 강제 치환 및 하드 검증
        tts_text, is_modified = validate_and_fix_tts_pronunciation(raw_tts_text)
        if is_modified:
            print(f"  - 🚨 [TTS 낭독 자동 교정] Scene {s_id}: '3AI' -> '쓰리에이아이' / 'AI' -> '에이아이' 독음 하드닝 적용")

        bg_prompt = scene.get("prompt")
        
        s_id_padded = f"{int(s_id):02d}"
        print(f"=== [Scene {s_id_padded}/{len(scenes)}] {scene.get('title', '')} ===")
        
        img_path = os.path.join(IMAGES_DIR, f"scene_{s_id_padded}.jpg")
        audio_path = os.path.join(OUTPUT_DIR, f"scene_{s_id_padded}.mp3")
        timing_path = os.path.join(OUTPUT_DIR, f"scene_{s_id_padded}_timing.json")
        
        # 1. 배경 이미지
        if not os.path.exists(img_path):
            print(f"  - 배경 이미지 생성 요청: {bg_prompt}")
            temp_img = os.path.join(IMAGES_DIR, f"temp_{s_id_padded}.jpg")
            success = generate_video_via_pollinations(bg_prompt, temp_img)
            if success and os.path.exists(temp_img):
                try:
                    bg = PILImage.open(temp_img).convert("RGBA")
                    target_w, target_h = 1920, 1080
                    bg_ratio = bg.width / bg.height
                    target_ratio = target_w / target_h
                    if bg_ratio > target_ratio:
                        new_w = int(bg.height * target_ratio)
                        offset = (bg.width - new_w) // 2
                        bg = bg.crop((offset, 0, offset + new_w, bg.height))
                    else:
                        new_h = int(bg.width / target_ratio)
                        offset = (bg.height - new_h) // 2
                        bg = bg.crop((0, offset, bg.width, offset + new_h))
                    bg = bg.resize((target_w, target_h), PILImage.Resampling.LANCZOS)
                    
                    overlay = PILImage.new("RGBA", (target_w, target_h), (0, 0, 0, int(255 * 0.6)))
                    base_img = PILImage.alpha_composite(bg, overlay).convert("RGB")
                    base_img.save(img_path, "JPEG")
                    if os.path.exists(temp_img): os.remove(temp_img)
                except Exception:
                    base_img = PILImage.new("RGB", (1920, 1080), (9, 13, 22))
                    base_img.save(img_path, "JPEG")
            else:
                base_img = PILImage.new("RGB", (1920, 1080), (9, 13, 22))
                base_img.save(img_path, "JPEG")
        else:
            print(f"  - 기존 배경 이미지 사용: {img_path}")
            
        # 2. TTS 생성 및 타임스탬프 (tts_text로 생성)
        if not os.path.exists(audio_path) or not os.path.exists(timing_path):
            await generate_tts_edge(tts_text, audio_path, timing_path)
        else:
            print(f"  - 기존 오디오 사용: {audio_path}")
            
        try:
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
            
            video = CompositeVideoClip([img_clip] + txt_clips)
            video = video.with_audio(audio_clip).with_duration(duration)
            
            clips.append(video)
        except Exception as e:
            error_msg = f"Scene {s_id} 비디오 클립 생성 실패: {e}"
            print(error_msg)
            sys.exit(1)
            
    if clips:
        print("\n==================================================")
        print("🎥 모든 씬 렌더링 완료. 최종 병합(Concat) 진행...")
        print("==================================================")
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(FINAL_VIDEO, fps=24, codec="libx264", audio_codec="aac", threads=4)
        print(f"\n🎉 [대성공] 본편 EP.03 낭독 교정 렌더링 완벽 완료! -> {FINAL_VIDEO}")

if __name__ == "__main__":
    asyncio.run(build_pipeline(force_clean_tts=False))
