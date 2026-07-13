import os
import numpy as np
import librosa
import json
from google.cloud import texttospeech
from dotenv import load_dotenv

# .env 로드
ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(ENV_PATH)

# 로컬 설정 파일 로드
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)["youtube_pipeline"]

# Google Cloud TTS API 키
API_KEY = os.environ.get("GOOGLE_TTS_API_KEY", "")

def generate_tts(text, output_path="output.mp3"):
    """
    Google Cloud Text-to-Speech로 프리미엄 한국어 음성 생성
    - 모델: ko-KR-Wavenet-D (남성 자연스러운 목소리)
    - Wavenet = 딥러닝 기반 고품질 TTS
    """
    print(f"[Audio Processor] Google Cloud TTS (Wavenet) 변환 시작...")

    client = texttospeech.TextToSpeechClient(
        client_options={"api_key": API_KEY} if API_KEY else None
    )

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # ko-KR-Wavenet-D: 한국어 남성 Wavenet 목소리
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.95,   # 살짝 천천히 (자연스러움)
        pitch=0.0,            # 기본 피치
        volume_gain_db=1.0,   # 약간 볼륨 업
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    with open(output_path, "wb") as f:
        f.write(response.audio_content)

    print(f"[Audio Processor] TTS 생성 완료: {output_path}")
    return output_path


def extract_waveform_data(audio_path, max_points=100):
    """librosa를 사용하여 오디오 파일에서 웨이브폼(주파수 진폭) 데이터 추출"""
    print(f"[Audio Processor] 웨이브폼 데이터 추출 중: {audio_path}")

    y, sr = librosa.load(audio_path, sr=None)

    frame_length = max(1024, len(y) // max_points)
    hop_length = frame_length

    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]

    if len(rms) > max_points:
        indices = np.linspace(0, len(rms) - 1, max_points, dtype=int)
        rms = rms[indices]

    if np.max(rms) > 0:
        rms = rms / np.max(rms)

    print(f"[Audio Processor] 웨이브폼 포인트 추출 완료 (총 {len(rms)}개)")
    return rms


if __name__ == "__main__":
    test_text = "안녕하세요. 3AI 유튜브 채널입니다. 구글 웨이브넷 목소리 테스트입니다."
    generate_tts(test_text, "test_wavenet.mp3")
