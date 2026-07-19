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
SELECTION_FILE = os.path.join(BASE_DIR, "manbok_selection.json")
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
    # Dummy implementation for telegram alert
    print(f"[텔레그램 전송 흉내] {msg}")
    pass

def phase_1_generate_candidates():
    print(">>> [Phase 1] 뽀개기 후보군 생성 (최대 15개)")
    
    # RSS 감지 실행
    subprocess.run(["python", WATCHER_SCRIPT], check=True)
    
    if not os.path.exists(QUEUE_FILE):
        print("큐 파일이 없습니다.")
        return
        
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)
        
    pending = queue.get("pending", [])
    if not pending:
        print("새로운 영상이 없습니다.")
        return
        
    channels = channel_manager.load_channels()
    def get_weight(item):
        c_name = item.get("channel_name", "")
        for cid, cinfo in channels.items():
            if cinfo.get("name") == c_name:
                return cinfo.get("weight", 1.0)
        return 1.0
        
    pending.sort(key=lambda x: get_weight(x), reverse=True)
    top_15 = pending[:15]
    
    date_compact = datetime.now().strftime("%Y%m%d")
    md_path = os.path.join(MESSAGES_DIR, f"자동→만복_{date_compact}_뽀개기후보목록.md")
    
    content = f"---\nstatus: unread\n---\n\n# 📋 오늘자 뽀개기 후보 목록\n\n**작성일:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n만복아, 아래 후보군 15개 중 뽀개기 진행할 영상 6개를 선별해서 `manbok_selection.json` 형식으로 기록해줘!\n\n"
    
    for idx, item in enumerate(top_15, 1):
        vid_id = item['video_id']
        title = item['title']
        c_name = item.get('channel_name', 'Unknown')
        content += f"**{idx}.** [{c_name}] {title}\n- 링크: https://youtu.be/{vid_id}\n- ID: `{vid_id}`\n\n"
        
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"후보 목록 생성 완료: {md_path}")
    send_telegram_msg("📋 오늘 뽀개기 후보 목록 도착. 6개 선택해주세요.")

def phase_2_execute_selection(selection_data):
    print(">>> [Phase 2] 만복 큐레이션 실행 (6건)")
    
    manbok_ids = selection_data.get("manbok", [])
    anti_ids = selection_data.get("anti", [])
    
    # Get details from QUEUE
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)
    pending = {item["video_id"]: item for item in queue.get("pending", [])}
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_compact = datetime.now().strftime("%Y%m%d")
    
    # 만복 담당 3건
    for vid_id in manbok_ids:
        item = pending.get(vid_id, {"title": f"Unknown_{vid_id}", "video_id": vid_id})
        title = item["title"]
        url = f"https://youtu.be/{vid_id}"
        transcript_path = os.path.join(BASE_DIR, "transcripts", f"Manbok_{vid_id}.txt")
        print(f"[만복] STT 추출 -> {title}")
        try:
            subprocess.run(["python", STT_SCRIPT, url, transcript_path], check=True)
            c.execute("INSERT OR REPLACE INTO pobbagi_history (video_id, title, pobbagi_date, assignee, status) VALUES (?, ?, ?, ?, ?)",
                      (vid_id, title, date_str, "manbok", "completed"))
        except Exception as e:
            print(f"STT 에러: {e}")
            c.execute("INSERT OR REPLACE INTO pobbagi_history (video_id, title, pobbagi_date, assignee, status) VALUES (?, ?, ?, ?, ?)",
                      (vid_id, title, date_str, "manbok", "error"))

    # 안티 담당 3건
    for idx, vid_id in enumerate(anti_ids, 1):
        item = pending.get(vid_id, {"title": f"Unknown_{vid_id}", "video_id": vid_id})
        title = item["title"]
        md_path = os.path.join(MESSAGES_DIR, f"만복→안티_{date_compact}_뽀개기{idx}번_지시.md")
        content = f"---\nstatus: unread\n---\n\n# [지시] 뽀개기 자동 할당 {idx}번\n\n**발신:** 만복 (자동화 파이프라인)\n**수신:** 안티\n\n**영상 제목:** {title}\n**URL:** https://youtu.be/{vid_id}\n\n안티야, 이 영상 자막 추출하고 Deep 서치 돌려서 기획안 뽑아줘!"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(content)
        c.execute("INSERT OR REPLACE INTO pobbagi_history (video_id, title, pobbagi_date, assignee, status) VALUES (?, ?, ?, ?, ?)",
                  (vid_id, title, date_str, "anti", "pending"))

    conn.commit()
    conn.close()
    
    # Cleanup selection file
    try:
        os.rename(SELECTION_FILE, SELECTION_FILE + f".{date_compact}.bak")
    except Exception as e:
        print(f"선택 파일 백업 실패: {e}")
        
    send_telegram_msg("🎯 오늘 뽀개기 준비 완료\n선택된 영상 6개 처리 끝. 귀가 후 리뷰 가능")
    
def run_daily_pobbagi():
    print("=== [Jarvis] 뽀개기 자동화 파이프라인 v2.1 (반자동 큐레이션) 시작 ===")
    init_db()
    
    if os.path.exists(SELECTION_FILE):
        with open(SELECTION_FILE, "r", encoding="utf-8") as f:
            try:
                selection_data = json.load(f)
                phase_2_execute_selection(selection_data)
                print("=== 파이프라인 완료 (Phase 2) ===")
            except json.JSONDecodeError:
                print("선택 파일 형식이 잘못되었습니다.")
    else:
        phase_1_generate_candidates()
        print("=== 파이프라인 완료 (Phase 1: 만복 선택 대기중) ===")

if __name__ == "__main__":
    run_daily_pobbagi()
