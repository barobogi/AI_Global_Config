import os
import json
import re
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

# ---------------------------------------------------------
# [Karpathy LLM Wiki / EmotionPrompt 헬퍼 모듈] (뽀개기 3번 연동)
# ---------------------------------------------------------

EMOTION_PROMPT = (
    "⚠️ [CRITICAL & HIGH-STAKES] 이 영상 분석 및 기획안은 3AI 핵심 지식 아키텍처에 직접 편입되는 주요 자산입니다. "
    "단 하나의 환각이나 누락 없이 최고의 분석력과 집중력으로 깊이 있게 도출하십시오."
)

TECH_KEYWORDS = [
    "LangGraph", "Pydantic", "NetworkX", "Karpathy", "VibeCoding", "Graphify", 
    "EmotionPrompt", "DevilsAdvocate", "RepoMix", "AutoSecurity", "HumanInTheLoop", 
    "Whisper", "Claude", "Obsidian", "Playwright", "LLM Wiki", "GPS Check"
]

def apply_emotion_prompt(text: str) -> str:
    """EmotionPrompt 기법을 프롬프트 및 지시서에 주입하여 LLM 분석 정확도를 극대화합니다."""
    return f"{EMOTION_PROMPT}\n\n{text}"

def extract_and_format_wiki_links(text: str) -> str:
    """
    Karpathy LLM Wiki 방식: 텍스트 내 핵심 기술 용어를 [[키워드]] 형태의 위키링크로 자동 변환합니다.
    """
    formatted_text = text
    for kw in TECH_KEYWORDS:
        # 대소문자 구분 없이 이미 [[...]] 형태로 작성되어 있지 않은 단어를 [[단어]]로 치환
        pattern = re.compile(rf"(?<!\[\[)\b({re.escape(kw)})\b(?!\]\])", re.IGNORECASE)
        formatted_text = pattern.sub(r"[[\1]]", formatted_text)
    return formatted_text

# ---------------------------------------------------------

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
    try:
        print(f"[텔레그램 전송 흉내] {msg}")
    except UnicodeEncodeError:
        print(msg.encode('cp949', errors='replace').decode('cp949'))

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
    
    raw_content = (
        f"# 📋 오늘자 뽀개기 후보 목록\n\n"
        f"**작성일:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"만복아, 아래 후보군 15개 중 뽀개기 진행할 영상 6개를 선별해서 `manbok_selection.json` 형식으로 기록해줘!\n\n"
    )
    
    for idx, item in enumerate(top_15, 1):
        vid_id = item['video_id']
        title = item['title']
        c_name = item.get('channel_name', 'Unknown')
        raw_content += f"**{idx}.** [{c_name}] {title}\n- 링크: https://youtu.be/{vid_id}\n- ID: `{vid_id}`\n\n"
        
    # Karpathy LLM Wiki 위키링크 치환 적용
    wiki_content = extract_and_format_wiki_links(raw_content)
    final_content = f"---\nstatus: unread\n---\n\n{wiki_content}"
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print(f"후보 목록 생성 완료 (LLM Wiki 연동): {md_path}")
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

    # 안티 담당 3건 (EmotionPrompt + LLM Wiki 적용)
    for idx, vid_id in enumerate(anti_ids, 1):
        item = pending.get(vid_id, {"title": f"Unknown_{vid_id}", "video_id": vid_id})
        title = item["title"]
        md_path = os.path.join(MESSAGES_DIR, f"만복→안티_{date_compact}_뽀개기{idx}번_지시.md")
        
        base_instructions = (
            f"# [지시] 뽀개기 자동 할당 {idx}번\n\n"
            f"**발신:** 만복 (자동화 파이프라인)\n**수신:** 안티\n\n"
            f"**영상 제목:** {title}\n**URL:** https://youtu.be/{vid_id}\n\n"
            f"## G (Goal)\n이 영상을 분석해 기술노트 뽀개기 8단계 프로세스(자막 추출→Deep 서치→저작권 확인)에 따라 기획안을 도출하고 Obsidian 지식베이스용 [[LLM Wiki]] 파이프라인을 적용한다.\n\n"
            f"## P (Proof)\n자막 텍스트 파일 + Deep 서치 결과 + 뿌리체계 편입 및 [[LLM Wiki]] 위키링크가 담긴 기획안 3종 세트가 만복에게 인계되고 pass 검증을 통과한다.\n\n"
            f"## S (Steps)\n1. yt-dlp로 자막 추출 (`transcripts/` 저장)\n2. `parallel_search.py`로 관련 사례/최신 정보 Deep 서치\n3. 저작권/출처 확인 (스터디 목적, 재가공 채널 발행 금지)\n4. 기획안 작성시 핵심 용어를 [[키워드]] 형태 위키링크로 연결\n5. 작성 완료 후 반드시 `python fact_checker.py --stt [STT경로] --summary [기획안경로]` 실행하여 PASS 검증\n6. 팩트체크 리포트(`.factcheck.md`)와 함께 코니 1차 검토 요청 → 만복 인계"
        )
        
        # 1) EmotionPrompt 적용
        emotion_applied = apply_emotion_prompt(base_instructions)
        # 2) Karpathy LLM Wiki 키워드 자동 위키링크 치환
        wiki_applied = extract_and_format_wiki_links(emotion_applied)
        
        content = f"---\nstatus: unread\n---\n\n{wiki_applied}"
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(content)

        gps_check = subprocess.run(
            ["python", os.path.join(r"D:\AI\Global_Define", "gps_check.py"), md_path],
            capture_output=True, text=True
        )
        if gps_check.returncode != 0:
            print(f"⚠️ GPS 검증 실패 — 지시서 발송 보류: {md_path}\n{gps_check.stdout}")
            os.rename(md_path, md_path + ".gps_rejected")
            continue

        c.execute("INSERT OR REPLACE INTO pobbagi_history (video_id, title, pobbagi_date, assignee, status) VALUES (?, ?, ?, ?, ?)",
                  (vid_id, title, date_str, "anti", "pending"))

    conn.commit()
    conn.close()
    
    # Update queue
    processed_ids = set(manbok_ids + anti_ids)
    new_pending = []
    for item in queue.get("pending", []):
        if item["video_id"] in processed_ids:
            queue.setdefault("processed", []).append(item)
        else:
            new_pending.append(item)
    queue["pending"] = new_pending
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=4)
    
    # Cleanup selection file
    try:
        if os.path.exists(SELECTION_FILE + f".{date_compact}.bak"):
            os.remove(SELECTION_FILE + f".{date_compact}.bak")
        os.rename(SELECTION_FILE, SELECTION_FILE + f".{date_compact}.bak")
    except Exception as e:
        print(f"선택 파일 백업 실패: {e}")
        
    send_telegram_msg("🎯 오늘 뽀개기 준비 완료\n선택된 영상 6개 처리 끝 (EmotionPrompt + LLM Wiki 연동 완료). 귀가 후 리뷰 가능")
    
def run_daily_pobbagi():
    print("=== [Jarvis] 뽀개기 자동화 파이프라인 v2.2 (EmotionPrompt + Karpathy LLM Wiki 연동) 시작 ===")
    init_db()
    
    if os.path.exists(SELECTION_FILE):
        selection_data = None
        with open(SELECTION_FILE, "r", encoding="utf-8") as f:
            try:
                selection_data = json.load(f)
            except json.JSONDecodeError:
                print("선택 파일 형식이 잘못되었습니다.")
                
        if selection_data:
            phase_2_execute_selection(selection_data)
            print("=== 파이프라인 완료 (Phase 2) ===")
    else:
        phase_1_generate_candidates()
        print("=== 파이프라인 완료 (Phase 1: 만복 선택 대기중) ===")

if __name__ == "__main__":
    run_daily_pobbagi()
