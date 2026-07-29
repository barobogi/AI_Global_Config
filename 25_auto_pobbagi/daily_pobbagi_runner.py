import os
import json
import re
import sqlite3
import subprocess
import sys
from datetime import datetime
import channel_manager
import youtube_transcript_extractor as yte

# Windows console 한글/이모지 출력 오류 방지
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = r"D:\AI\25_auto_pobbagi"
# 2026-07-18 D:\AI\.venv가 user PATH에서 C:\hb보다 우선순위가 높아져 bare "python" 호출이
# pydantic/google-genai 없는 빈 venv로 새버리는 문제 발견(2026-07-30) → 표준 인터프리터 명시 고정
PYTHON_EXE = r"C:\hb\python.exe"
DB_FILE = os.path.join(BASE_DIR, "pobbagi_history.db")
STT_SCRIPT = os.path.join(BASE_DIR, "auto_stt_gemini.py")
SEARCH_SCRIPT = r"D:\AI\Global_Define\parallel_search.py"
WATCHER_SCRIPT = os.path.join(BASE_DIR, "youtube_rss_watcher.py")
QUEUE_FILE = os.path.join(BASE_DIR, "youtube_queue.json")
SELECTION_FILE = os.path.join(BASE_DIR, "manbok_selection.json")
MESSAGES_DIR = r"D:\AI\AI_hub\shared\messages"

# Graphify 노드 저장 경로 (아키텍처개선 6번 / 뿌리 31 연동)
GRAPHIFY_NODE_DIR = r"D:\AI\31_graphify\graphify-out"
GRAPHIFY_NODE_FILE = os.path.join(GRAPHIFY_NODE_DIR, "wiki_nodes.json")

# ---------------------------------------------------------
# [Karpathy LLM Wiki / EmotionPrompt 헬퍼 모듈] (뽀개기 3번 연동 개정판)
# ---------------------------------------------------------

# 기획안 충실 이행: 초보자 친절 멘토 페르소나 + EmotionPrompt 분석 프롬프트
EMOTION_MENTOR_PROMPT = (
    "당신은 초보 개발자에게 친절하고 세심하게 가르쳐주는 따뜻한 멘토이자 3AI 시스템의 핵심 분석가입니다.\n"
    "⚠️ [CRITICAL MEMORY & HIGH STAKES] 이 분석 결과는 3AI 지식 아키텍처와 바로보기님의 세컨드 브레인에 직접 편입되는 소중한 지식 자산입니다.\n"
    "단 하나의 오개념이나 환각 없이 최고 수준의 정교함과 친절함으로 핵심 내용을 분석하고 정리해 주십시오.\n\n"
)

TECH_KEYWORDS = [
    "LangGraph", "Pydantic", "NetworkX", "Karpathy", "VibeCoding", "Graphify", 
    "EmotionPrompt", "DevilsAdvocate", "RepoMix", "AutoSecurity", "HumanInTheLoop", 
    "Whisper", "Claude", "Obsidian", "Playwright", "LLM Wiki", "GPS Check", "Agent Memory", "CodeGraph"
]

def build_summary_prompt(instruction_text: str) -> str:
    """만복 지시서 전달 시 안티의 친절한 멘토 EmotionPrompt 및 지식 아키텍처 맥락을 전면에 결합합니다."""
    header = (
        f"{EMOTION_MENTOR_PROMPT}"
        f"안티는 초보 개발자에게 세심하게 설명하는 친절한 멘토의 시각으로 아래 지시사항 및 기술 뽀개기 8단계 프로세스를 완수하십시오:\n\n"
    )
    return f"{header}{instruction_text}"

def register_graphify_nodes(wiki_keywords: list):
    """추출된 위키 키워드를 Graphify 지식 노드 DB/파일(wiki_nodes.json)에 등록하여 실질 지식망으로 연결합니다."""
    os.makedirs(GRAPHIFY_NODE_DIR, exist_ok=True)
    existing_nodes = {}
    if os.path.exists(GRAPHIFY_NODE_FILE):
        try:
            with open(GRAPHIFY_NODE_FILE, "r", encoding="utf-8") as f:
                existing_nodes = json.load(f)
        except Exception:
            existing_nodes = {}
            
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for kw in wiki_keywords:
        if kw not in existing_nodes:
            existing_nodes[kw] = {
                "label": kw,
                "type": "WikiConcept",
                "created_at": now_str,
                "connected_root": 31
            }
            
    with open(GRAPHIFY_NODE_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_nodes, f, ensure_ascii=False, indent=2)

def extract_and_link_graphify_nodes(text: str) -> str:
    """
    Karpathy LLM Wiki 방식:
    1) 텍스트 내 핵심 기술 용어를 [[키워드]] 형태 위키링크로 변환 (한글 조사 경계 처리 유연화)
    2) 추출된 키워드들을 Graphify 지식망 노드로 실질 등록/연동
    """
    formatted_text = text
    found_keywords = []
    
    for kw in TECH_KEYWORDS:
        # 한글 조사와 붙어있어도 매칭 가능하도록 (?<!\[\[)kw(?!\]\])
        pattern = re.compile(rf"(?<!\[\[)({re.escape(kw)})(?!\]\])", re.IGNORECASE)
        if pattern.search(formatted_text):
            found_keywords.append(kw)
            formatted_text = pattern.sub(r"[[\1]]", formatted_text)
            
    if found_keywords:
        register_graphify_nodes(found_keywords)
        
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
    
    subprocess.run([PYTHON_EXE, WATCHER_SCRIPT], check=True)
    
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
        
    wiki_content = extract_and_link_graphify_nodes(raw_content)
    final_content = f"---\nstatus: unread\n---\n\n{wiki_content}"
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print(f"후보 목록 생성 완료 (LLM Wiki & Graphify 노드 실질 연동): {md_path}")
    send_telegram_msg("📋 오늘 뽀개기 후보 목록 도착. 6개 선택해주세요.")

def phase_2_execute_selection(selection_data):
    print(">>> [Phase 2] 만복 큐레이션 실행 (6건)")
    
    manbok_ids = selection_data.get("manbok", [])
    anti_ids = selection_data.get("anti", [])
    
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)
    pending = {item["video_id"]: item for item in queue.get("pending", [])}
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_compact = datetime.now().strftime("%Y%m%d")
    
    for vid_id in manbok_ids:
        item = pending.get(vid_id, {"title": f"Unknown_{vid_id}", "video_id": vid_id})
        title = item["title"]
        url = f"https://youtu.be/{vid_id}"
        transcript_path = os.path.join(BASE_DIR, "transcripts", f"Manbok_{vid_id}.txt")

        # 2026-07-30: 자막 추출(youtube-transcript-api) 1순위 -> 실패 시 Gemini Flash STT 2순위 폴백
        # (Gemini STT 자체는 API 키 이슈로 별도 점검 필요 — 일요일 확인 예정)
        print(f"[만복] 자막 추출(1순위) -> {title}")
        extracted_path = yte.extract_transcript(vid_id)
        if extracted_path:
            with open(extracted_path, "r", encoding="utf-8") as rf:
                text = rf.read()
            with open(transcript_path, "w", encoding="utf-8") as wf:
                wf.write(text)
            c.execute("INSERT OR REPLACE INTO pobbagi_history (video_id, title, pobbagi_date, assignee, status) VALUES (?, ?, ?, ?, ?)",
                      (vid_id, title, date_str, "manbok", "completed"))
            continue

        print(f"[만복] 자막 실패 -> Gemini STT(2순위) 폴백 -> {title}")
        try:
            subprocess.run([PYTHON_EXE, STT_SCRIPT, url, transcript_path], check=True)
            c.execute("INSERT OR REPLACE INTO pobbagi_history (video_id, title, pobbagi_date, assignee, status) VALUES (?, ?, ?, ?, ?)",
                      (vid_id, title, date_str, "manbok", "completed"))
        except Exception as e:
            print(f"STT 에러: {e}")
            c.execute("INSERT OR REPLACE INTO pobbagi_history (video_id, title, pobbagi_date, assignee, status) VALUES (?, ?, ?, ?, ?)",
                      (vid_id, title, date_str, "manbok", "error"))

    for idx, vid_id in enumerate(anti_ids, 1):
        item = pending.get(vid_id, {"title": f"Unknown_{vid_id}", "video_id": vid_id})
        title = item["title"]
        md_path = os.path.join(MESSAGES_DIR, f"만복→안티_{date_compact}_뽀개기{idx}번_지시.md")
        
        base_instructions = (
            f"# [지시] 뽀개기 자동 할당 {idx}번\n\n"
            f"**발신:** 만복 (자동화 파이프라인)\n**수신:** 안티\n\n"
            f"**영상 제목:** {title}\n**URL:** https://youtu.be/{vid_id}\n\n"
            f"## G (Goal)\n이 영상을 분석해 기술노트 뽀개기 8단계 프로세스(자막 추출→Deep 서치→저작권 확인)에 따라 기획안을 도출하고 Obsidian 및 [[Graphify]] 연동용 [[LLM Wiki]] 파이프라인을 적용한다.\n\n"
            f"## P (Proof)\n자막 텍스트 파일 + Deep 서치 결과 + [[Graphify]] 노드로 연동된 [[LLM Wiki]] 기획안 3종 세트가 만복에게 인계되고 pass 검증을 통과한다.\n\n"
            f"## S (Steps)\n1. yt-dlp로 자막 추출 (`transcripts/` 저장)\n2. `parallel_search.py`로 관련 사례/최신 정보 Deep 서치\n3. 저작권/출처 확인 (스터디 목적, 재가공 채널 발행 금지)\n4. 친절한 멘토 EmotionPrompt를 적용하여 기획안 작성 및 핵심 용어를 [[키워드]] 형태 위키링크로 연결\n5. 작성 완료 후 반드시 `python fact_checker.py --stt [STT경로] --summary [기획안경로]` 실행하여 PASS 검증\n6. 팩트체크 리포트(`.factcheck.md`)와 함께 코니 1차 검토 요청 → 만복"
        )
        
        # 1) EmotionPrompt 멘토 템플릿 실제 호출 연동
        emotion_applied = build_summary_prompt(base_instructions)
        # 2) Karpathy LLM Wiki 키워드 자동 위키링크 치환 및 Graphify 노드 연동
        wiki_applied = extract_and_link_graphify_nodes(emotion_applied)
        content = f"---\nstatus: unread\n---\n\n{wiki_applied}"
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(content)

        gps_check = subprocess.run(
            [PYTHON_EXE, os.path.join(r"D:\AI\Global_Define", "gps_check.py"), md_path],
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
    
    try:
        if os.path.exists(SELECTION_FILE + f".{date_compact}.bak"):
            os.remove(SELECTION_FILE + f".{date_compact}.bak")
        os.rename(SELECTION_FILE, SELECTION_FILE + f".{date_compact}.bak")
    except Exception as e:
        print(f"선택 파일 백업 실패: {e}")
        
    send_telegram_msg("🎯 오늘 뽀개기 준비 완료\n선택된 영상 6개 처리 끝 (EmotionPrompt + LLM Wiki & Graphify 연동 완료). 귀가 후 리뷰 가능")
    
def run_daily_pobbagi():
    print("=== [Jarvis] 뽀개기 자동화 파이프라인 v2.3 (EmotionPrompt 멘토 + Karpathy LLM Wiki Graphify 실질 연동) 시작 ===")
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
