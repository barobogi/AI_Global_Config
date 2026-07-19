import os
import subprocess
import json
import glob

QUEUE_FILE = r"D:\AI\25_auto_pobbagi\youtube_queue.json"
OUTPUT_DIR = r"D:\AI\25_auto_pobbagi\transcripts"

def extract_transcript(video_id):
    """
    yt-dlp를 사용하여 자막을 추출합니다.
    사용자의 Chrome 브라우저 쿠키를 자동으로 가져와 429 차단을 우회합니다.
    (Chrome 대신 Edge를 주로 쓰신다면 'edge'로 변경 가능합니다.)
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    output_template = os.path.join(OUTPUT_DIR, f"{video_id}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # yt-dlp 명령어 구성 (자막만 다운로드, 영상 제외)
    # --cookies-from-browser chrome 를 통해 현재 로그인된 세션 활용
    cmd = [
        "yt-dlp",
        "--skip-download",          # 영상 다운로드 생략
        "--write-auto-subs",        # 자동 생성 자막
        "--write-subs",             # 수동 생성 자막
        "--sub-lang", "ko,en",      # 한국어, 영어 우선
        "--sub-format", "vtt",      # VTT 포맷
        "--cookies", r"D:\AI\25_auto_pobbagi\cookies.txt", # ★ 핵심: 추출된 cookies.txt 활용
        "-o", output_template,
        url
    ]
    
    print(f"[{video_id}] 자막 추출 시도 중... (Chrome 쿠키 활용)")
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 다운로드된 vtt 파일 찾기
        vtt_files = glob.glob(f"{output_template}*.vtt")
        if vtt_files:
            print(f"[{video_id}] 자막 추출 성공: {vtt_files[0]}")
            return vtt_files[0]
        else:
            print(f"[{video_id}] 자막 파일을 찾을 수 없습니다. (지원되지 않는 영상일 수 있음)")
            return None
    except subprocess.CalledProcessError as e:
        print(f"[{video_id}] yt-dlp 자막 추출 실패: {e}")
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
            # 실패 시 다시 pending 유지 (또는 에러 처리)
            vid["status"] = "failed"
            remaining.append(vid)
            
    queue["pending"] = remaining
    
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=4)
        
    print("=== 자막 추출 작업 종료 ===")

if __name__ == "__main__":
    run_extractor()
