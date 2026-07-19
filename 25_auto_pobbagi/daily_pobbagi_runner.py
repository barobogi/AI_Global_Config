import os
import json
import sqlite3
import subprocess
from datetime import datetime
import channel_manager

BASE_DIR = r"D:\AI\25_auto_pobbagi"
DB_FILE = os.path.join(BASE_DIR, "pobbagi_history.db")
STT_SCRIPT = os.path.join(BASE_DIR, "auto_stt_gemini.py")
SEARCH_SCRIPT = r"D:\AI\Global_Define\parallel_search.py"
WATCHER_SCRIPT = os.path.join(BASE_DIR, "youtube_rss_watcher.py")
QUEUE_FILE = os.path.join(BASE_DIR, "youtube_queue.json")
MESSAGES_DIR = r"D:\AI\AI_hub\shared\messages"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pobbagi_history (
            video_id TEXT PRIMARY KEY,
            title TEXT,
            channel_id TEXT,
            channel_name TEXT,
            pobbagi_date TEXT,
            assignee TEXT,
            status TEXT,
            root_id INTEGER,
            score REAL
        )
    ''')
    conn.commit()
    conn.close()

def send_telegram_msg(msg):
    # Dummy implementation for telegram alert, since telegram_messages.py is missing or not reachable
    print(f"[텔레그램 전송 흉내] {msg}")
    pass

def run_daily_pobbagi():
    print("=== [Jarvis] 뽀개기 자동화 파이프라인 v2.0 시작 ===")
    init_db()
    
    # 1. RSS 감지 실행
    subprocess.run(["python", WATCHER_SCRIPT], check=True)
    
    # 2. 큐 로드
    if not os.path.exists(QUEUE_FILE):
        print("큐 파일이 없습니다.")
        return
        
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)
        
    pending = queue.get("pending", [])
    if not pending:
        print("새로운 영상이 없습니다.")
        return
        
    # 가중치 기반 정렬 로직 (여기서는 단순 상위 6개 선택)
    channels = channel_manager.load_channels()
    def get_weight(item):
        c_name = item.get("channel_name", "")
        # channel name matching to weight
        for cid, cinfo in channels.items():
            if cinfo.get("name") == c_name:
                return cinfo.get("weight", 1.0)
        return 1.0
        
    pending.sort(key=lambda x: get_weight(x), reverse=True)
    top_6 = pending[:6]
    
    manbok_items = top_6[:3]
    anti_items = top_6[3:6]
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_compact = datetime.now().strftime("%Y%m%d")
    
    # 만복 담당 STT
    print(">>> 만복 STT 추출 시작 (3건)")
    for item in manbok_items:
        vid_id = item["video_id"]
        title = item["title"]
        url = f"https://youtu.be/{vid_id}"
        transcript_path = os.path.join(BASE_DIR, "transcripts", f"Manbok_{vid_id}.txt")
        print(f"  -> {title}")
        try:
            subprocess.run(["python", STT_SCRIPT, url, transcript_path], check=True)
            c.execute("INSERT OR REPLACE INTO pobbagi_history (video_id, title, pobbagi_date, assignee, status) VALUES (?, ?, ?, ?, ?)",
                      (vid_id, title, date_str, "manbok", "completed"))
        except Exception as e:
            print(f"STT 에러: {e}")
            c.execute("INSERT OR REPLACE INTO pobbagi_history (video_id, title, pobbagi_date, assignee, status) VALUES (?, ?, ?, ?, ?)",
                      (vid_id, title, date_str, "manbok", "error"))

    # 안티 지시서 생성
    print(">>> 안티 지시서 생성 (3건)")
    for idx, item in enumerate(anti_items, 1):
        vid_id = item["video_id"]
        title = item["title"]
        md_path = os.path.join(MESSAGES_DIR, f"만복→안티_{date_compact}_뽀개기{idx}번_지시.md")
        content = f"---\nstatus: unread\n---\n\n# [지시] 뽀개기 자동 할당 {idx}번\n\n**발신:** 만복 (자동화 파이프라인)\n**수신:** 안티\n\n**영상 제목:** {title}\n**URL:** https://youtu.be/{vid_id}\n\n안티야, 이 영상 자막 추출하고 Deep 서치 돌려서 기획안 뽑아줘!"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(content)
        c.execute("INSERT OR REPLACE INTO pobbagi_history (video_id, title, pobbagi_date, assignee, status) VALUES (?, ?, ?, ?, ?)",
                  (vid_id, title, date_str, "anti", "pending"))

    conn.commit()
    conn.close()
    
    # 텔레그램 발송
    titles_str = "\n".join([f"- {v['title']}" for v in top_6])
    msg = f"🎯 오늘 뽀개기 준비 완료\n{titles_str}\n귀가 후 리뷰 가능"
    send_telegram_msg(msg)
    
    # 격발 스크립트 실행
    push_script = r"D:\AI\Global_Define\push_to_all.py"
    if os.path.exists(push_script):
        subprocess.Popen(["python", push_script])
        
    print("=== 자동화 파이프라인 v2.0 완료 ===")

if __name__ == "__main__":
    run_daily_pobbagi()
