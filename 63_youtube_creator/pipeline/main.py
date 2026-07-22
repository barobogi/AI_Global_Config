import os
import json
import asyncio
from PIL import Image, ImageDraw
from moviepy import AudioFileClip, ImageSequenceClip
import numpy as np

# 모듈 임포트
from audio_processor import generate_tts, extract_waveform_data
from video_renderer import create_frame, WIDTH, HEIGHT, VISUAL
from study_scraper import get_latest_study_posts, post_to_script
from pollinations_auto import generate_video_via_pollinations

def main(script_text, output_filename="final_output.mp4", bg_prompt=None):
    print(f"========== [T063] 유튜브 파이프라인 엔진 시작 ==========")
    
    # 0. 배경 이미지 생성 (Kling AI) 및 전처리 캐싱
    base_img = None
    if bg_prompt:
        temp_bg = "temp_bg.jpg"
        print(f"[Main] Pollinations.ai 배경 이미지 생성 요청: {bg_prompt}")
        success = generate_video_via_pollinations(bg_prompt, temp_bg)
        if success and os.path.exists(temp_bg):
            try:
                bg = Image.open(temp_bg).convert("RGBA")
                # 종횡비 유지하면서 꽉 차게 리사이즈 및 크롭 (Center Crop)
                bg_ratio = bg.width / bg.height
                target_ratio = WIDTH / HEIGHT
                if bg_ratio > target_ratio:
                    new_w = int(bg.height * target_ratio)
                    offset = (bg.width - new_w) // 2
                    bg = bg.crop((offset, 0, offset + new_w, bg.height))
                else:
                    new_h = int(bg.width / target_ratio)
                    offset = (bg.height - new_h) // 2
                    bg = bg.crop((0, offset, bg.width, offset + new_h))
                bg = bg.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
                
                # 가독성을 위한 Dimming (검은색 60% 반투명 레이어)
                overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, int(255 * 0.6)))
                base_img = Image.alpha_composite(bg, overlay).convert("RGB")
                print("[Main] 배경 이미지 전처리(Dimming) 및 캐싱 완료.")
            except Exception as e:
                print(f"[Main] 배경 이미지 전처리 실패: {e}")
                base_img = None
        else:
            print("[Main] 배경 이미지 생성 실패. 단색 배경으로 진행합니다.")
            
    # 1. 오디오 처리 (TTS 생성 및 웨이브폼 추출)
    temp_audio = "temp_audio.mp3"
    generate_tts(script_text, temp_audio)
    
    # 오디오 길이(초) 파악
    audio_clip = AudioFileClip(temp_audio)
    duration = audio_clip.duration
    
    # 총 프레임 수 계산 (초 * FPS)
    fps = VISUAL["fps"]
    total_frames = int(duration * fps)
    
    # 프레임 수만큼 웨이브폼 데이터 포인트 추출
    wave_data = extract_waveform_data(temp_audio, max_points=total_frames)
    
    # 2. 비디오 렌더링 (프레임 이미지 배열 생성)
    print(f"[Main] 비디오 프레임 렌더링 시작... (총 {total_frames} 프레임, FPS: {fps})")
    frames = []
    
    # 타자기 효과를 위해 텍스트 청크 단위 계산
    for i in range(total_frames):
        if i % 30 == 0:
            print(f"   -> 프레임 렌더링 중: {i}/{total_frames}")
        
        # 각 프레임마다의 웨이브폼 데이터 (전체 데이터에서 주변 30개 포인트만 샘플링하여 움직임 표현)
        window_size = 50
        start_idx = max(0, i - window_size // 2)
        end_idx = min(len(wave_data), i + window_size // 2)
        
        # 화면에 그릴 50개 포인트 유지 (제로 패딩)
        current_wave = np.zeros(window_size)
        slice_len = end_idx - start_idx
        
        if slice_len > 0:
            # 중앙 정렬
            pad_start = (window_size - slice_len) // 2
            current_wave[pad_start:pad_start+slice_len] = wave_data[start_idx:end_idx]
            
        frame_img = create_frame(script_text, current_wave, i, total_frames, base_img=base_img)
        frames.append(frame_img)
        
    print("[Main] 프레임 렌더링 완료. 영상 합성(Encoding) 시작...")
    
    # 3. 오디오와 비디오 합성 (MoviePy)
    video_clip = ImageSequenceClip(frames, fps=fps)
    video_clip = video_clip.with_audio(audio_clip)
    
    # 결과물 출력 (H.264 코덱 사용)
    video_clip.write_videofile(
        output_filename, 
        codec="libx264", 
        audio_codec="aac", 
        temp_audiofile="temp-audio.m4a", 
        remove_temp=True,
        logger=None # MoviePy의 장황한 기본 로그 숨김
    )
    
    # 임시 오디오 파일 삭제
    if os.path.exists(temp_audio):
        os.remove(temp_audio)
        
    print(f"========== [T063] 파이프라인 엔진 완료: {output_filename} ==========")

if __name__ == "__main__":
    # AI Study 최신 게시글 자동 수집
    print("[Pipeline] AI Study 최신 게시글 수집 중...")
    posts = get_latest_study_posts(count=1)
    
    if not posts:
        print("[Pipeline] 게시글을 찾을 수 없습니다.")
        exit(1)
    
    latest = posts[0]
    print(f"[Pipeline] 게시글 선택: [{latest['id']}] {latest['title']}")
    
    script = post_to_script(latest)
    output_file = f"output_{latest['id']}.mp4"
    
    main(script, output_file)
