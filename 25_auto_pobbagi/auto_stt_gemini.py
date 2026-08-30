import os
import sys
import json
import time
import subprocess
from google import genai

def get_api_key():
    # 2026-08-30: config.json에 평문 커밋되어 6주간 public 저장소 노출된 사고 발견 →
    # 환경변수 우선, 없으면 .env(gitignore 대상) 파일에서 읽도록 변경.
    env_key = os.environ.get('GEMINI_API_KEY')
    if env_key:
        return env_key
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('GEMINI_API_KEY='):
                    return line.split('=', 1)[1].strip()
    return None

def extract_subtitle(video_url, output_txt_path):
    api_key = get_api_key()
    if not api_key:
        print('Error: GEMINI_API_KEY not found in config.json')
        sys.exit(1)

    video_id = video_url.split('/')[-1].split('?v=')[-1]
    audio_path = f'temp_{video_id}.m4a'
    
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        print(f'Downloading audio for {video_url}...')
        subprocess.run(['yt-dlp', '--cookies', 'D:/AI/25_auto_pobbagi/cookies.txt', '-f', 'bestaudio[ext=m4a]', video_url, '-o', audio_path], check=True)
        
        print('Audio downloaded. Uploading to Gemini...')
        client = genai.Client(api_key=api_key)
        audio_file = client.files.upload(file=audio_path)
        
        print('Transcribing (with exponential backoff)...')
        max_retries = 3
        base_delay = 2
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[audio_file, '이 오디오의 내용을 한국어 자막 형태(전체 텍스트)로 추출해줘. 요약하지 말고 들리는 대로 전부 다 적어줘.']
                )
                break # Success
            except Exception as e:
                print(f'Attempt {attempt+1} failed: {e}')
                if attempt == max_retries - 1:
                    raise
                time.sleep(base_delay * (2 ** attempt))
        
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f'Done! Saved to {output_txt_path}')
        
    finally:
        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python auto_stt_gemini.py <video_url> <output_txt_path>')
        sys.exit(1)
    extract_subtitle(sys.argv[1], sys.argv[2])
