import os
import numpy as np
import librosa
from openai import OpenAI
import json

from dotenv import load_dotenv

# 로컬 설정 파일 로드
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)["youtube_pipeline"]

# .env 파일 로드
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

# OpenAI API 키 (환경 변수에서 로드 또는 직접 입력 필요)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "YOUR_API_KEY_HERE":
    raise ValueError("OpenAI API Key가 설정되지 않았습니다. .env 파일에 OPENAI_API_KEY를 입력해주세요.")

client = OpenAI(api_key=api_key)

def generate_tts(text, output_path="output.mp3"):
    """OpenAI TTS를 사용하여 텍스트를 음성으로 변환"""
    print(f"[Audio Processor] TTS 생성 중... (Voice: {config['tts_settings']['voice']})")
    
    response = client.audio.speech.create(
        model="tts-1",
        voice=config['tts_settings']['voice'],
        input=text,
        speed=config['tts_settings']['speed']
    )
    
    response.stream_to_file(output_path)
    print(f"[Audio Processor] TTS 생성 완료: {output_path}")
    return output_path

def extract_waveform_data(audio_path, max_points=100):
    """librosa를 사용하여 오디오 파일에서 웨이브폼(주파수 진폭) 데이터 추출"""
    print(f"[Audio Processor] 웨이브폼 데이터 추출 중: {audio_path}")
    
    # 오디오 로드 (sr=None으로 원래 샘플레이트 유지)
    y, sr = librosa.load(audio_path, sr=None)
    
    # 전체 오디오를 max_points 개수의 구간으로 나누어 RMS 진폭 계산
    # frame_length를 오디오 길이에 맞게 동적으로 설정
    frame_length = max(1024, len(y) // max_points)
    hop_length = frame_length
    
    # RMS(Root Mean Square) 에너지 추출
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    
    # 너무 많은 포인트가 나오면 샘플링해서 max_points에 맞춤
    if len(rms) > max_points:
        indices = np.linspace(0, len(rms) - 1, max_points, dtype=int)
        rms = rms[indices]
        
    # 정규화 (0.0 ~ 1.0)
    if np.max(rms) > 0:
        rms = rms / np.max(rms)
        
    print(f"[Audio Processor] 웨이브폼 포인트 추출 완료 (총 {len(rms)}개)")
    return rms

if __name__ == "__main__":
    # 간단한 테스트 스크립트
    test_text = "안녕하세요! 3AI 유튜브 채널 자동화 테스트입니다."
    test_audio = "test_audio.mp3"
    
    try:
        generate_tts(test_text, test_audio)
        wave_data = extract_waveform_data(test_audio, max_points=50)
        print("웨이브폼 데이터 샘플:", wave_data[:5])
    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")
