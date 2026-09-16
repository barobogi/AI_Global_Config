"""
바로보기 세컨드 브레인 + 3AI 실시간 채팅 통합 백엔드 API (FastAPI)
- 모바일 앱(안드로이드) & 웹 대시보드 단일 통합 허브
- 로컬 PC 환경 및 Render.com 클라우드 무중단 듀얼 환경 지원
- 포트: 8765 (로컬), $PORT (Render)
"""

import os
import sys
import glob
import json
import sqlite3
import uuid
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from fastapi import FastAPI, Query, HTTPException, WebSocket, WebSocketDisconnect, UploadFile, File, Form, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel

_LOCAL_REALTIME_DIR = r"D:\AI\43_function_dev\01_realtime_3ai"
if os.path.isdir(_LOCAL_REALTIME_DIR):
    sys.path.insert(0, _LOCAL_REALTIME_DIR)
    from realtime_engine import Realtime3AIEngine, _get_agent_secret
else:
    # Render 등 로컬 PC 경로가 없는 클라우드 환경 - 3AI 채팅 트리거만 비활성화(no-op), 나머지 API는 정상 동작
    class Realtime3AIEngine:
        def send_message(self, *args, **kwargs):
            return None

        def save_message(self, *args, **kwargs):
            return None

    def _get_agent_secret(name):
        return None

engine_3ai = Realtime3AIEngine()
CLINE_WEBHOOK_TOKEN = os.environ.get("CLINE_SESSION_TOKEN") or _get_agent_secret("cline")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# -------------------------------------------------------------
# 1. 경로 듀얼 폴백 해석 (로컬 우선, 클라우드 환경에서는 ./data)
# -------------------------------------------------------------
RENDER_DIR = BASE_DIR / "renders"
RENDER_DIR.mkdir(parents=True, exist_ok=True)


LOCAL_PLAN_PATH = Path("D:/AI/63_youtube_creator/pipeline/daily_briefing/weekly_plan.json")
PLAN_PATH = LOCAL_PLAN_PATH if LOCAL_PLAN_PATH.exists() else (DATA_DIR / "weekly_plan.json")

LOCAL_TRANSCRIPTS_DIR = Path("D:/AI/25_auto_pobbagi/transcripts")
TRANSCRIPTS_DIR = LOCAL_TRANSCRIPTS_DIR if LOCAL_TRANSCRIPTS_DIR.exists() else (DATA_DIR / "transcripts")

LOCAL_DB_PATH = Path("D:/AI/43_function_dev/01_realtime_3ai/realtime_3ai.db")
DB_PATH = LOCAL_DB_PATH if LOCAL_DB_PATH.exists() else (DATA_DIR / "realtime_3ai.db")

LOCAL_QUEUE_PATH = Path("D:/AI/23_infra/notebook_pending_queue.json")
QUEUE_PATH = LOCAL_QUEUE_PATH if LOCAL_QUEUE_PATH.exists() else (DATA_DIR / "notebook_pending_queue.json")

UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# DB 연결 헬퍼
def get_db_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn

# -------------------------------------------------------------
# 2. WebSocket 실시간 브로드캐스트 매니저
# -------------------------------------------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            "manbok": [],
            "kony": [],
            "anti": [],
            "human": []
        }

    async def connect(self, websocket: WebSocket, agent_name: str):
        await websocket.accept()
        if agent_name not in self.active_connections:
            self.active_connections[agent_name] = []
        self.active_connections[agent_name].append(websocket)
        print(f"[Hub] '{agent_name}' connected to WebSocket stream.")

    def disconnect(self, websocket: WebSocket, agent_name: str):
        if agent_name in self.active_connections and websocket in self.active_connections[agent_name]:
            self.active_connections[agent_name].remove(websocket)
            print(f"[Hub] '{agent_name}' disconnected.")

    async def broadcast_live_message(self, payload: dict):
        for name, sockets in self.active_connections.items():
            for ws in sockets:
                try:
                    await ws.send_json(payload)
                except Exception:
                    pass

manager = ConnectionManager()

# -------------------------------------------------------------
# 3. FastAPI 앱 및 생명주기
# -------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[SecondBrain] Unified Backend Started.")
    print(f"  - RENDER_DIR: {RENDER_DIR} (exists: {RENDER_DIR.exists()})")
    print(f"  - PLAN_PATH: {PLAN_PATH} (exists: {PLAN_PATH.exists()})")
    print(f"  - DB_PATH: {DB_PATH} (exists: {DB_PATH.exists()})")
    yield
    print("[SecondBrain] Unified Backend Stopped.")

app = FastAPI(
    title="Barobogi Second Brain & 3AI Real-Time Hub API",
    version="2.0.0",
    description="통합 세컨드 브레인 모바일 백엔드 & 3AI 실시간 채팅 허브",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/static/renders/{filename:path}")
def serve_renders_file(filename: str):
    target = RENDER_DIR / filename
    if not target.exists():
        creator_target = Path("D:/AI/63_youtube_creator/pipeline/daily_briefing/renders") / filename
        if creator_target.exists():
            target = creator_target
        else:
            raise HTTPException(status_code=404, detail="File not found")
    media_type = "application/vnd.android.package-archive" if filename.endswith(".apk") else None
    return FileResponse(path=str(target), media_type=media_type)

app.mount("/static/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")


# -------------------------------------------------------------
# 4. 데이터 모델 정의
# -------------------------------------------------------------
class ShareRequest(BaseModel):
    url: str
    title: str = ""
    comment: str = ""

class SendMessageRequest(BaseModel):
    sender: str
    recipient: str = "all"
    content: str
    conversation_id: str = "general_live"
    tier: int = 1
    metadata: Optional[dict] = None
    auth_token: Optional[str] = None

# -------------------------------------------------------------
# 5. 세컨드 브레인 API 라우트
# -------------------------------------------------------------
@app.get("/")
@app.get("/health")
@app.get("/api/health")
@app.get("/api/v1/health")
def health_check():
    return {
        "status": "OK",
        "service": "Barobogi Second Brain & 3AI Real-Time Hub API",
        "timestamp": datetime.now().isoformat(),
        "db": "Connected" if DB_PATH.exists() else "Cloud (No Local DB)"
    }

V18_APK_PATH = Path("D:/AI/65_android_apps/barobogi_second_brain/SecondBrain_v1.8.apk")

@app.get("/download/v1.8")
@app.get("/download/SecondBrain_v1.8.apk")
@app.get("/download/app-debug.apk")
@app.get("/download/SecondBrain_v1.7.apk")
@app.get("/download/latest")
@app.get("/dl")
def download_second_brain_v18_apk():
    target = V18_APK_PATH
    if not target.exists():
        target = Path("D:/AI/65_android_apps/barobogi_second_brain/android/app/build/outputs/apk/debug/app-debug.apk")
    if not target.exists():
        raise HTTPException(status_code=404, detail="SecondBrain v1.8 APK file not found")
    
    file_size = target.stat().st_size
    return FileResponse(
        path=str(target),
        filename="SecondBrain_v1.8.apk",
        content_disposition_type="attachment",
        media_type="application/octet-stream",
        headers={
            "Content-Length": str(file_size),
            "Accept-Ranges": "bytes"
        }
    )



@app.get("/api/v1/briefings/latest")
def get_latest_briefing(target_date: str = None):
    """지정된 날짜(기본값: 오늘)의 3AI 일일 오디오 브리핑 정보 반환"""
    if not PLAN_PATH.exists():
        raise HTTPException(status_code=404, detail="No weekly plan generated yet")
        
    with open(PLAN_PATH, "r", encoding="utf-8") as f:
        plan = json.load(f)
        
    if not plan:
        raise HTTPException(status_code=404, detail="Empty briefing plan")
        
    from datetime import timezone, timedelta
    KST = timezone(timedelta(hours=9))
    today_str = target_date or datetime.now(KST).strftime("%Y-%m-%d")
    
    matched = None
    for item in plan:
        if item.get("date") == today_str:
            matched = item
            break
            
    if not matched:
        past_items = [item for item in plan if item.get("date", "") <= today_str]
        if past_items:
            matched = past_items[-1]
        else:
            matched = plan[0]
            
    ep_id = matched["episode_id"]
    audio_filename = f"{ep_id}_audio.mp3"
    video_filename = f"{ep_id}.mp4"
    
    return {
        "episode_id": ep_id,
        "date": matched["date"],
        "day": matched["day"],
        "topic": matched["topic"],
        "audio_url": f"/static/renders/{audio_filename}",
        "video_url": f"/static/renders/{video_filename}",
        "dialogue": matched["dialogue"]
    }

def parse_clean_knowledge_content(content: str) -> str:
    """트랜스크립트 파일에서 동영상 정보 메타데이터 및 STT 지침 문구를 제외한 순수 지식 노하우 본문만 추출"""
    lines = content.splitlines()
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if any(stripped.startswith(prefix) for prefix in [
            "[동영상 정보]", "제목:", "URL:", "출처 채널:", "NotebookLM Source ID:",
            "글자수:", "추출일시:", "[자막 및 트랜스크립트 전문]", "이 오디오의 내용을", "한국어 자막"
        ]):
            continue
        clean_lines.append(stripped)
    return " ".join(clean_lines)

SUMMARIES_PATH = DATA_DIR / "knowledge_summaries.json"

@app.get("/api/v1/knowledge/list")
def list_all_knowledge():
    """184개 실데이터 지식 DB 전수 목록 반환 (Gemini 2.5 Flash 3-Tier 지식 DB 반영)"""
    if SUMMARIES_PATH.exists():
        try:
            with open(SUMMARIES_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            items = data.get("items", [])
            for item in items:
                item["audio_url"] = f"/api/v1/knowledge/audio/{item['id']}"
                if "snippet" not in item:
                    item["snippet"] = item.get("three_line_summary", "")[:200]
            return {"total_entries": len(items), "items": items}
        except Exception:
            pass

    items = []
    if TRANSCRIPTS_DIR.exists():
        files = sorted(glob.glob(os.path.join(str(TRANSCRIPTS_DIR), "*.txt")) + glob.glob(os.path.join(str(TRANSCRIPTS_DIR), "*.vtt")))
        for filepath in files:
            try:
                fname = os.path.basename(filepath)
                ext = fname.split(".")[-1]
                title = fname
                snippet = ""
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    raw_content = f.read(3000)
                    for line in raw_content.splitlines()[:6]:
                        if line.startswith("제목:"):
                            title = line.replace("제목:", "").strip()
                            break
                    clean_body = parse_clean_knowledge_content(raw_content)
                    snippet = clean_body[:200]
                items.append({
                    "id": fname,
                    "title": title,
                    "ext": ext,
                    "snippet": snippet,
                    "audio_url": f"/api/v1/knowledge/audio/{fname}"
                })
            except Exception:
                continue
    return {"total_entries": len(items), "items": items}

@app.get("/api/v1/knowledge/audio/{item_id:path}")
async def get_knowledge_item_audio(item_id: str):
    """지식 DB 특정 항목 전용 1분 앵커 TTS 동적 합성 및 스트리밍 서빙"""
    title = item_id
    tts_text = ""

    if SUMMARIES_PATH.exists():
        try:
            with open(SUMMARIES_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data.get("items", []):
                if item.get("id") == item_id or item.get("id") == f"{item_id}.txt":
                    title = item.get("title", item_id)
                    tts_text = item.get("tts_script", "")
                    break
        except Exception:
            pass

    if not tts_text:
        target_file = TRANSCRIPTS_DIR / item_id
        if not target_file.exists():
            target_file = TRANSCRIPTS_DIR / f"{item_id}.txt"
        if target_file.exists():
            try:
                with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
                    raw_content = f.read(3000)
                    for line in raw_content.splitlines()[:6]:
                        if line.startswith("제목:"):
                            title = line.replace("제목:", "").strip()
                            break
                    clean_body = parse_clean_knowledge_content(raw_content)
                    tts_text = f"지식 DB 항목. {title}. 요약 노하우: {clean_body[:250]}"
            except Exception:
                pass

    if not tts_text:
        tts_text = f"지식 DB 항목. {title}"

    safe_name = "".join([c if c.isalnum() else "_" for c in item_id])
    cached_mp3 = RENDER_DIR / f"item_tts_v3_{safe_name}.mp3"
    
    if not cached_mp3.exists() or cached_mp3.stat().st_size == 0:
        import edge_tts
        processed_text = tts_text.replace("3AI", "쓰리에이아이").replace("AI", "에이아이").replace("DB", "디비").replace("API", "에이피아이")
        communicate = edge_tts.Communicate(processed_text, "ko-KR-HyunsuMultilingualNeural", rate="+2%")
        await communicate.save(str(cached_mp3))

    return FileResponse(path=str(cached_mp3), media_type="audio/mpeg", filename=f"{safe_name}.mp3")


@app.get("/api/v1/knowledge/search")
def search_knowledge(q: str = Query(..., min_length=1)):
    """지식 풀텍스트 및 키워드/요약 검색"""
    results = []
    q_lower = q.lower()

    if SUMMARIES_PATH.exists():
        try:
            with open(SUMMARIES_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data.get("items", []):
                text_to_search = f"{item.get('title', '')} {' '.join(item.get('keywords', []))} {item.get('three_line_summary', '')} {item.get('deep_insights', '')} {item.get('category', '')}"
                if q_lower in text_to_search.lower():
                    results.append({
                        "file": item.get("title", item.get("id")),
                        "id": item.get("id"),
                        "category": item.get("category", ""),
                        "snippet": item.get("three_line_summary", "")[:200],
                        "audio_url": f"/api/v1/knowledge/audio/{item['id']}"
                    })
            if results:
                return {"query": q, "total_matches": len(results), "results": results}
        except Exception:
            pass

    if TRANSCRIPTS_DIR.exists():
        files = glob.glob(os.path.join(str(TRANSCRIPTS_DIR), "*.txt"))
        for filepath in files:
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if q_lower in content.lower():
                        title = os.path.basename(filepath)
                        for line in content.splitlines()[:6]:
                            if line.startswith("제목:"):
                                title = line.replace("제목:", "").strip()
                                break
                                
                        idx = content.lower().find(q_lower)
                        snippet = content[max(0, idx - 40): min(len(content), idx + 160)]
                        results.append({
                            "file": title,
                            "id": os.path.basename(filepath),
                            "snippet": snippet,
                            "audio_url": f"/api/v1/knowledge/audio/{os.path.basename(filepath)}"
                        })
            except Exception:
                continue
    return {"query": q, "total_matches": len(results), "results": results}


@app.post("/api/v1/knowledge/share")
def ingest_shared_item(req: ShareRequest):
    """모바일에서 '공유하기'로 전송된 URL을 NotebookLM 큐에 적재"""
    queue = []
    if QUEUE_PATH.exists():
        try:
            with open(QUEUE_PATH, "r", encoding="utf-8") as f:
                queue = json.load(f)
        except Exception:
            queue = []
            
    item = {
        "url": req.url,
        "title": req.title or req.url,
        "comment": req.comment,
        "source": "mobile_share_target",
        "timestamp": datetime.now().isoformat()
    }
    queue.append(item)
    
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)
        
    return {"status": "SUCCESS", "message": "URL queued for 3AI Second Brain ingestion"}

# -------------------------------------------------------------
# 6. 실시간 3AI 채팅 API 라우트 (hub_server 통합)
# -------------------------------------------------------------
@app.get("/chat", response_class=HTMLResponse)
def get_chat_ui():
    ui_path = BASE_DIR / "chat_ui.html"
    if ui_path.exists():
        return ui_path.read_text(encoding="utf-8")
    return "<h1>Chat UI Not Found</h1>"

@app.get("/api/history")
def get_chat_history(limit: int = 50):
    """실시간 채팅 이력 조회"""
    if not DB_PATH.exists():
        return {"messages": []}
    with get_db_connection() as conn:
        cursor = conn.execute(
            "SELECT * FROM messages ORDER BY id DESC LIMIT ?", (limit,)
        )
        rows = [dict(r) for r in cursor.fetchall()]
        rows.reverse()
        return {"messages": rows}

@app.post("/api/v1/chat/sync")
async def sync_chat_messages(request: Request):
    """로컬 3AI DB 메시지를 Render 클라우드 백엔드로 실시간/배치 동기화 수신"""
    try:
        payload = await request.json()
        msgs = payload.get("messages", [])
        if not msgs:
            return {"status": "ok", "synced": 0}

        synced_count = 0
        with get_db_connection() as conn:
            for m in msgs:
                try:
                    meta_str = m.get("metadata")
                    if isinstance(meta_str, dict):
                        meta_str = json.dumps(meta_str, ensure_ascii=False)
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO messages (msg_id, conversation_id, sender, recipient, content, tier, status, metadata, created_at, auth_signature, log_hash)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            m.get("msg_id"),
                            m.get("conversation_id", "general"),
                            m.get("sender"),
                            m.get("recipient", "all"),
                            m.get("content"),
                            m.get("tier", 1),
                            m.get("status", "read"),
                            meta_str or "{}",
                            m.get("created_at"),
                            m.get("auth_signature", "0" * 64),
                            m.get("log_hash", "0" * 64)
                        )
                    )
                    synced_count += 1
                except Exception:
                    continue
            conn.commit()
        return {"status": "ok", "synced": synced_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cline/webhook")
async def cline_webhook(request: Request, authorization: Optional[str] = Header(None)):
    """Cline 확장(saoudrizwan.claude-dev)의 TaskStart/PostToolUse/TaskComplete 훅이 쏘는 이벤트 수신.
    ~/Documents/Cline/webhook_config.json 의 webhook_token과 Bearer 매칭 필수 - 안 맞으면 401."""
    expected = f"Bearer {CLINE_WEBHOOK_TOKEN}"
    if not authorization or authorization != expected:
        raise HTTPException(status_code=401, detail="invalid webhook token")

    payload = await request.json()
    event = payload.get("event", "unknown")
    data = payload.get("data", {})
    task_id = data.get("task_id", "?")

    # tool_executed(PostToolUse)는 도구 호출마다 발생해 채팅 스팸이 되므로 수신만 하고 릴레이하지 않음
    if event not in ("task_started", "task_completed"):
        return {"status": "ok", "relayed": False}

    label = {
        "task_started": "작업 시작",
        "task_completed": "작업 완료",
    }.get(event, event)

    content = (
        f"[Cline - {label}] task_id={task_id}\n"
        f"(git에 커밋되었는지, cline 전용 폴더 안에서만 작업했는지 확인 필요 - 자동 알림일 뿐 검증은 아님)"
    )
    engine_3ai.send_message(
        sender="cline",
        recipient="all",
        content=content,
        conversation_id="general_live",
        tier=1,
        auth_token=CLINE_WEBHOOK_TOKEN,
    )
    return {"status": "ok"}


# -------------------------------------------------------------
# 6-1. 안전한 이미지 파일 업로드 API (코니 4대 보안 체크포인트 준수)
# -------------------------------------------------------------
ALLOWED_IMAGE_SIGNATURES = {
    b"\xFF\xD8\xFF": ".jpg",
    b"\x89PNG\r\n\x1a\n": ".png",
    b"GIF87a": ".gif",
    b"GIF89a": ".gif",
    b"RIFF": ".webp" # RIFF....WEBP
}
MAX_FILE_SIZE = 10 * 1024 * 1024 # 10MB

@app.post("/api/upload")
async def upload_image_file(file: UploadFile = File(...)):
    """
    채팅 이미지 첨부용 보안 엔드포인트
    1. 서버 측 파일 크기 하드 리밋(10MB) 강제 (DoS 차단)
    2. 서버 측 매직 바이트 검증 (.html/.svg 위장 stored XSS 차단)
    3. 원본 파일명 완전 폐기 및 서버 UUID 파일명 신규 생성 (경로 트래버설 원천 차단)
    4. 보안 검증 통과한 파일만 정적 서빙 경로에 격리 저장
    """
    # 1. 크기 확인 및 청크 스트림 읽기
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File exceeds maximum allowed size of 10MB (Received: {len(content)} bytes)")

    if len(content) < 12:
        raise HTTPException(status_code=400, detail="Invalid file: empty or too small")

    # 2. 매직 바이트 시그니처 정밀 검증
    detected_ext = None
    if content.startswith(b"\xFF\xD8\xFF"):
        detected_ext = ".jpg"
    elif content.startswith(b"\x89PNG\r\n\x1a\n"):
        detected_ext = ".png"
    elif content.startswith(b"GIF87a") or content.startswith(b"GIF89a"):
        detected_ext = ".gif"
    elif content.startswith(b"RIFF") and content[8:12] == b"WEBP":
        detected_ext = ".webp"

    if not detected_ext:
        raise HTTPException(
            status_code=400,
            detail="Security Verification Failed: Unsupported file type or invalid magic bytes. Only genuine JPG, PNG, GIF, WEBP images are allowed."
        )

    # 3. UUID 기반 고유 파일명 생성 (원본 파일명 사용 금지로 트래버설 원천 방지)
    secure_filename = f"img_{uuid.uuid4().hex}{detected_ext}"
    target_path = (UPLOADS_DIR / secure_filename).resolve()

    # 경로 탈출 방지 확인 (Sanitize Check)
    if not str(target_path).startswith(str(UPLOADS_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Path traversal attempt detected")

    # 4. 파일 저장
    with open(target_path, "wb") as f:
        f.write(content)

    relative_url = f"/static/uploads/{secure_filename}"
    return {
        "status": "success",
        "filename": secure_filename,
        "url": relative_url,
        "size_bytes": len(content),
        "content_type": f"image/{detected_ext.lstrip('.')}"
    }

@app.post("/send")
async def send_message_http(req: SendMessageRequest):
    """메시지 전송 (human 또는 AI) - 3AI 파이프라인 출처 증명 및 3중 가드레일 정식 연동"""
    auth_tok = req.auth_token
    if not auth_tok and req.sender.lower() == "human":
        auth_tok = "token_human_direct_2026_super_secure"

    try:
        msg_id = engine_3ai.send_message(
            sender=req.sender,
            recipient=req.recipient,
            content=req.content,
            conversation_id=req.conversation_id,
            tier=req.tier,
            metadata=req.metadata,
            auth_token=auth_tok
        )
    except Exception as ex:
        print(f"[Main Backend] send_message error: {ex}")
        raise HTTPException(status_code=400, detail=str(ex))

    local_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    out_payload = {
        "event": "new_message",
        "msg_id": msg_id,
        "sender": req.sender,
        "recipient": req.recipient,
        "content": req.content,
        "conversation_id": req.conversation_id,
        "tier": req.tier,
        "created_at": local_time_str
    }
    await manager.broadcast_live_message(out_payload)

    # 2026-09-10: 별도 웨이크업 트리거 호출 제거 - engine_3ai.send_message() 안의
    # _dispatch_popup_trigger()가 이미 모든 수신자에게 동일한 트리거를 쏘고 있어서
    # 여기서 또 쏘면 코니/안티 창에 같은 메시지가 2번 붙여넣어지는 버그였음
    # (realtime_engine.py의 send_message 참고, 트리거 경로는 이제 그쪽 하나뿐).

    return {"status": "success", "msg_id": msg_id}

@app.websocket("/ws/{agent_name}")
async def websocket_endpoint(websocket: WebSocket, agent_name: str):
    await manager.connect(websocket, agent_name)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg_payload = json.loads(data)
                msg_type = msg_payload.get("type") or msg_payload.get("event")

                # 1. Ping-Pong Heartbeat Protocol
                if msg_type == "ping":
                    await websocket.send_json({"event": "pong", "timestamp": datetime.now().isoformat()})
                    continue
                elif msg_type == "pong":
                    continue

                sender = agent_name
                recipient = msg_payload.get("recipient", "all")
                content = msg_payload.get("content", "")
                conv_id = msg_payload.get("conversation_id", "general_live")
                tier = int(msg_payload.get("tier", 1))

                auth_tok = msg_payload.get("auth_token")
                if not auth_tok and sender.lower() == "human":
                    auth_tok = "token_human_direct_2026_super_secure"

                msg_id = engine_3ai.send_message(
                    sender=sender,
                    recipient=recipient,
                    content=content,
                    conversation_id=conv_id,
                    tier=tier,
                    metadata=msg_payload.get("metadata"),
                    auth_token=auth_tok
                )

                local_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                out_payload = {
                    "event": "new_message",
                    "msg_id": msg_id,
                    "sender": sender,
                    "recipient": recipient,
                    "content": content,
                    "conversation_id": conv_id,
                    "tier": tier,
                    "created_at": local_time_str
                }
                await manager.broadcast_live_message(out_payload)
                # NOTE: trigger_ai_agents_on_human_message는 /send HTTP 엔드포인트에서만 호출.
                # WS 경로는 AI 에이전트 세션이 직접 메시지를 올리는 경로라
                # human 트리거가 중복 발사되는 버그를 방지하기 위해 여기서는 호출하지 않음.
            except Exception as e:
                await websocket.send_json({"event": "error", "detail": str(e)})
    except WebSocketDisconnect:
        manager.disconnect(websocket, agent_name)

@app.get("/dl-hodu")
async def download_hodu_apk():
    apk_path = Path("D:/AI/65_android_apps/hodu_ai/android/app/build/outputs/apk/debug/app-debug.apk")
    if not apk_path.exists():
        raise HTTPException(status_code=404, detail="Hodu AI APK NOT FOUND.")
    return FileResponse(
        path=apk_path,
        media_type="application/vnd.android.package-archive",
        filename="HoduAI_v0.2.apk"
    )

@app.get("/dl-video")
async def download_video():
    video_path = Path("D:/AI/AutoVideo_Final.mp4")
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video NOT FOUND.")
    return FileResponse(
        path=video_path,
        media_type="video/mp4",
        filename="AutoVideo_Final.mp4"
    )

@app.get("/dl")
async def download_apk():
    apk_path = Path("D:/AI/65_android_apps/barobogi_second_brain/android/app/build/outputs/apk/debug/app-debug.apk")
    if not apk_path.exists():
        raise HTTPException(status_code=404, detail="APK 파일이 존재하지 않습니다.")
    return FileResponse(
        path=apk_path,
        filename="app-debug.apk",
        media_type="application/vnd.android.package-archive"
    )

LEARNING_REVIEW_DIR = Path("D:/AI/65_android_apps/hodu_ai/learning_review")
LEARNING_REVIEW_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/learning_review")
async def receive_learning_data(request: Request):
    """Android 호두AI 앱에서 수집한 학습 데이터(텍스트+음성 경로)를 수신"""
    try:
        payload = await request.json()
        count = payload.get("count", 0)
        device = payload.get("device", "unknown")
        app_ver = payload.get("appVersion", "?")
        examples = payload.get("examples", [])

        # 파일로 저장
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = LEARNING_REVIEW_DIR / f"learning_{ts}.json"
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        audio_count = sum(1 for ex in examples if ex.get("hasAudio"))

        # 3AI 실시간 채팅에 알림
        notify_msg = (
            f"📚 [호두AI 학습 데이터 도착]\n"
            f"기기: {device} | 버전: v{app_ver}\n"
            f"총 {count}건 수신 (음성 포함: {audio_count}건)\n"
            f"저장 위치: {save_path.name}\n"
            f"→ 3AI 검토 요청: D:/AI/65_android_apps/hodu_ai/learning_review/"
        )
        try:
            engine_3ai.save_message("시스템", notify_msg)
        except Exception:
            pass

        return JSONResponse({"status": "ok", "received": count, "saved": str(save_path.name)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8090))
    uvicorn.run(app, host="0.0.0.0", port=port)
