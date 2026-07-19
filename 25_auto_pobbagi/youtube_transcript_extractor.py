import os
import json
from youtube_transcript_api import YouTubeTranscriptApi

QUEUE_FILE = r"D:\AI\25_auto_pobbagi\youtube_queue.json"
OUTPUT_DIR = r"D:\AI\25_auto_pobbagi\transcripts"
COOKIES_FILE = r"D:\AI\25_auto_pobbagi\cookies.txt"

def extract_transcript(video_id):
    """
    youtube-transcript-api를 사용하여 자막을 추출합니다.
    사용자가 추출해 둔 cookies.txt를 활용하여 429 차단을 우회합니다.
    """
    output_path = os.path.join(OUTPUT_DIR, f"{video_id}.txt")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"[{video_id}] 자막 추출 시도 중... (youtube-transcript-api + cookies.txt)")
    try:
        # 쿠키 파일을 사용하여 자막 리스트 가져오기
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, cookies=COOKIES_FILE)
        
        # 한국어 자막(수동 또는 자동) 가져오기 시도, 없으면 영어
        try:
            transcript = transcript_list.find_transcript(['ko', 'en'])
        except:
            # 지정된 언어가 없으면 가능한 아무 언어나 번역해서(한국어로) 가져오기 시도
            transcript = transcript_list.find_transcript(['ko']).translate('ko')
            
        # 자막 데이터 페치 (리스트 형태의 딕셔너리)
        transcript_data = transcript.fetch()
        
        # 순수 텍스트만 추출해서 이어붙이기
        clean_text = " ".join([item['text'] for item in transcript_data])
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(clean_text)
            
        print(f"[{video_id}] 자막 추출 및 텍스트 변환 성공: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"[{video_id}] 자막 추출 실패: {e}")
        return None

def run_extractor():
    if not os.path.exists(QUEUE_FILE):
        print("대기열 파일이 없습니다.")
        return
        
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)
        
    pending = queue.get("pending", [])
    if not pending:
        print("추출 대기 중인 영상이 없습니다.")
        return
        
    print(f"총 {len(pending)}개의 영상에 대해 자막 추출을 시작합니다.")
    
    remaining = []
    for vid in pending:
        video_id = vid["video_id"]
        result_file = extract_transcript(video_id)
        
        if result_file:
            # 성공 시 processed로 이동
            vid["transcript_path"] = result_file
            vid["status"] = "extracted"
            queue.setdefault("processed", []).append(vid)
        else:
            # 실패 시 다시 pending 유지
            vid["status"] = "failed"
            remaining.append(vid)
            
    queue["pending"] = remaining
    
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=4)
        
    print("=== 자막 추출 작업 종료 ===")

if __name__ == "__main__":
    run_extractor()
