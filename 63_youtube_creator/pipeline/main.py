import os
import json
from moviepy import AudioFileClip, ImageSequenceClip
import numpy as np

# 모듈 임포트
from audio_processor import generate_tts, extract_waveform_data
from video_renderer import create_frame, WIDTH, HEIGHT, VISUAL

def main(script_text, output_filename="final_output.mp4"):
    print(f"========== [T063] 유튜브 파이프라인 엔진 시작 ==========")
    
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
            
        frame_img = create_frame(script_text, current_wave, i, total_frames)
        frames.append(frame_img)
        
    print("[Main] 프레임 렌더링 완료. 영상 합성(Encoding) 시작...")
    
    # 3. 오디오와 비디오 합성 (MoviePy)
    video_clip = ImageSequenceClip(frames, fps=fps)
    video_clip = video_clip.set_audio(audio_clip)
    
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
    # 테스트 실행
    sample_script = "안녕하세요. 3AI 유튜브 자동화 테스트 영상입니다. 지금 보시는 이 영상은 오직 파이썬 코드만으로 텍스트에서 영상까지 한 번에 렌더링 된 결과물입니다. 글씨가 타이핑되는 효과와, 제 목소리에 맞춰서 바닥에서 춤추는 웨이브폼 파형이 보이시나요? 디자인 템플릿만 자유롭게 바꾸면, 앞으로 3AI가 리서치한 자료를 단 1분 만에 유튜브 쇼츠로 찍어낼 수 있습니다."
    
    main(sample_script, "test_output.mp4")
