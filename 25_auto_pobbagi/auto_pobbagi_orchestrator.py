import os
import json
import subprocess
from datetime import datetime

# ==========================================
# 3AI 뽀개기 100% 자동화 오케스트레이터
# ==========================================
# Stage 1: 채널 감지 및 큐잉 (youtube_rss_watcher.py 호출)
# Stage 2: 병렬 분석 (Anti - STT, Manbok - Deep Search)
# Stage 3: 사용자 리뷰 대기 상태로 전환
# ==========================================

BASE_DIR = r"D:\AI\25_auto_pobbagi"
QUEUE_FILE = os.path.join(BASE_DIR, "youtube_queue.json")
STT_SCRIPT = os.path.join(BASE_DIR, "auto_stt_gemini.py")
SEARCH_SCRIPT = r"D:\AI\Global_Define\parallel_search.py"

def load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"pending": [], "processed": [], "waiting_review": []}

def save_queue(queue_data):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue_data, f, ensure_ascii=False, indent=4)

def run_stage1_watcher():
    print(">>> [Stage 1] 채널 자동 감지 및 큐잉 시작...")
    watcher_script = os.path.join(BASE_DIR, "youtube_rss_watcher.py")
    subprocess.run(["python", watcher_script], check=True)

def run_stage2_analysis():
    print(">>> [Stage 2] 안티/만복 병렬 분석 시작...")
    queue = load_queue()
    pending = queue.get("pending", [])
    
    if not pending:
        print(">>> 분석할 PENDING 아이템이 없습니다.")
        return
    
    # 안티 담당 3개, 만복 담당 3개 분배 (여기서는 순차적으로 배분)
    anti_items = pending[:3]
    manbok_items = pending[3:6]
    
    print(f">>> 안티 담당: {len(anti_items)}건, 만복 담당: {len(manbok_items)}건")
    
    # [Anti Role] - STT 추출
    for item in anti_items:
        vid_id = item["video_id"]
        title = item["title"]
        print(f"  [Anti] 자막 추출 시작: {title} ({vid_id})")
        url = f"https://youtu.be/{vid_id}"
        transcript_path = os.path.join(BASE_DIR, "transcripts", f"Anti_{vid_id}.txt")
        api_key = "AQ.Ab8RN6LufZgpf1zlTE4sZV6ASoj50ir0nRhl4z7nm4bmM-3bjA"
        
        try:
            subprocess.run(["python", STT_SCRIPT, url, transcript_path, api_key], check=True)
            item["anti_stt_path"] = transcript_path
            item["status"] = "waiting_review"
        except Exception as e:
            print(f"  [Anti 오류] {e}")
            item["status"] = "error"
            
    # [Manbok Role] - Deep Search
    for item in manbok_items:
        vid_id = item["video_id"]
        title = item["title"]
        print(f"  [Manbok] 딥 서치 시작: {title} ({vid_id})")
        
        try:
            search_cmd = ["python", SEARCH_SCRIPT, "--queries", title, "--max", "3"]
            subprocess.run(search_cmd, capture_output=True, text=True, check=True)
            item["manbok_search_result"] = "SUCCESS" 
            item["status"] = "waiting_review"
        except Exception as e:
            print(f"  [Manbok 오류] {e}")
            item["status"] = "error"

    # 처리된 항목 이동
    new_pending = []
    waiting_review = queue.get("waiting_review", [])
    
    for item in pending:
        if item["status"] == "waiting_review":
            waiting_review.append(item)
        elif item["status"] == "error":
            new_pending.append(item)
        else:
            new_pending.append(item)
            
    queue["pending"] = new_pending
    queue["waiting_review"] = waiting_review
    save_queue(queue)
    print(">>> [Stage 2] 병렬 분석 완료.")

def run_orchestrator():
    print("="*50)
    print(" 3AI 유튜브 뽀개기 100% 자동화 파이프라인 가동 ")
    print("="*50)
    
    run_stage1_watcher()
    run_stage2_analysis()
    
    queue = load_queue()
    waiting_count = len(queue.get("waiting_review", []))
    print(f">>> [Stage 3] 사용자 리뷰 대기 상태 아이템 수: {waiting_count}건")
    if waiting_count > 0:
        print(">>> 사용자(바로보기님)께 보고 후 승인(PASS)을 받아야 코니 검증으로 넘어갑니다.")

if __name__ == "__main__":
    run_orchestrator()
