"""
3AI Real-Time Local Pub/Sub Hub Server (FastAPI + WebSockets + Web Live Dashboard)
Project: 43_function_dev/01_realtime_3ai
Author: Anti (Operator)
"""

import sys
import json
import asyncio
import threading
from typing import Dict, List
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

# UTF-8 stdout wrapper
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from realtime_engine import Realtime3AIEngine, CircuitBreakerOpenError
from real_llm_debate import call_agent_llm, PERSONAS

db_engine = Realtime3AIEngine()

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
        db_engine.update_heartbeat(agent_name, status="online")
        print(f"[Hub] '{agent_name}' connected to WebSocket stream.")

    def disconnect(self, websocket: WebSocket, agent_name: str):
        if agent_name in self.active_connections and websocket in self.active_connections[agent_name]:
            self.active_connections[agent_name].remove(websocket)
            if not self.active_connections[agent_name]:
                db_engine.update_heartbeat(agent_name, status="offline")
            print(f"[Hub] '{agent_name}' disconnected.")

    async def broadcast_live_message(self, payload: dict):
        """Broadcast live message to ALL connected agents and human monitors instantly (<5ms)."""
        for name, sockets in self.active_connections.items():
            for ws in sockets:
                try:
                    await ws.send_json(payload)
                except Exception:
                    pass

manager = ConnectionManager()

# Request Models
class SendMessageRequest(BaseModel):
    sender: str
    recipient: str
    content: str
    conversation_id: str = "general"
    tier: int = 1
    metadata: dict = None

class StartDebateRequest(BaseModel):
    topic: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[Hub] 3AI Real-Time Pub/Sub Hub Server Started on http://127.0.0.1:8000")
    yield
    print("[Hub] 3AI Real-Time Pub/Sub Hub Server Stopped.")

app = FastAPI(
    title="3AI Real-Time Live Hub",
    version="2.0.0",
    description="Low-latency (<5ms) multi-agent WebSocket broker, SQLite WAL persistence, and live dashboard",
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"status": "running", "service": "3AI Real-Time Live Hub", "chat_ui": "http://127.0.0.1:8000/chat"}

@app.get("/chat", response_class=HTMLResponse)
def get_chat_ui():
    ui_path = BASE_DIR / "chat_ui.html"
    if ui_path.exists():
        return ui_path.read_text(encoding="utf-8")
    return "<h1>Chat UI Not Found</h1>"

@app.get("/api/history")
def get_chat_history(limit: int = 50):
    with db_engine._get_connection() as conn:
        cursor = conn.execute(
            "SELECT * FROM messages ORDER BY id ASC LIMIT ?", (limit,)
        )
        return {"messages": [dict(r) for r in cursor.fetchall()]}

@app.websocket("/ws/{agent_name}")
async def websocket_endpoint(websocket: WebSocket, agent_name: str):
    await manager.connect(websocket, agent_name)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg_payload = json.loads(data)
                sender = agent_name
                recipient = msg_payload.get("recipient", "all")
                content = msg_payload.get("content", "")
                conversation_id = msg_payload.get("conversation_id", "general")
                tier = int(msg_payload.get("tier", 1))
                
                msg_id = db_engine.send_message(
                    sender=sender,
                    recipient=recipient,
                    content=content,
                    conversation_id=conversation_id,
                    tier=tier
                )
                
                out_payload = {
                    "event": "new_message",
                    "msg_id": msg_id,
                    "sender": sender,
                    "recipient": recipient,
                    "content": content,
                    "conversation_id": conversation_id,
                    "tier": tier
                }
                await manager.broadcast_live_message(out_payload)
            except Exception as e:
                await websocket.send_json({"event": "error", "detail": str(e)})
    except WebSocketDisconnect:
        manager.disconnect(websocket, agent_name)

@app.post("/send")
async def send_message_http(req: SendMessageRequest):
    try:
        msg_id = db_engine.send_message(
            sender=req.sender,
            recipient=req.recipient,
            content=req.content,
            conversation_id=req.conversation_id,
            tier=req.tier,
            metadata=req.metadata
        )
        out_payload = {
            "event": "new_message",
            "msg_id": msg_id,
            "sender": req.sender,
            "recipient": req.recipient,
            "content": req.content,
            "conversation_id": req.conversation_id,
            "tier": req.tier
        }
        await manager.broadcast_live_message(out_payload)
        return {"status": "success", "msg_id": msg_id}
    except CircuitBreakerOpenError as cbe:
        raise HTTPException(status_code=429, detail=str(cbe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _run_real_llm_debate_background(topic: str):
    """Background runner for 3AI real-time LLM debate with live broadcast."""
    conv_id = f"web_debate_{int(asyncio.get_event_loop_policy().get_event_loop().time() if False else 1)}"
    history = []
    
    # Broadcast debate start
    asyncio.run(manager.broadcast_live_message({"event": "debate_started", "topic": topic}))
    
    # Turn 1: Manbok (Planner)
    history.append({"role": "user", "content": f"주제 '{topic}'에 대해 3AI 토론을 시작해 주세요."})
    manbok_t1 = call_agent_llm(PERSONAS["manbok"], history)
    history.append({"role": "assistant", "content": f"[만복]: {manbok_t1}"})
    db_engine.send_message("manbok", "all", manbok_t1, conversation_id=topic, tier=1)
    asyncio.run(manager.broadcast_live_message({
        "event": "new_message", "sender": "manbok", "recipient": "all", "content": manbok_t1
    }))

    # Turn 2: Anti (Operator)
    history.append({"role": "user", "content": "만복 형님의 제안을 바탕으로 기술 구현자(안티) 입장에서 기술적 실현 방안과 DB/파이프라인 연계 의견을 제시해 주세요."})
    anti_t2 = call_agent_llm(PERSONAS["anti"], history)
    history.append({"role": "assistant", "content": f"[안티]: {anti_t2}"})
    db_engine.send_message("anti", "all", anti_t2, conversation_id=topic, tier=1)
    asyncio.run(manager.broadcast_live_message({
        "event": "new_message", "sender": "anti", "recipient": "all", "content": anti_t2
    }))

    # Turn 3: Kony (Auditor)
    history.append({"role": "user", "content": "만복 형님과 안티의 발언을 검토하여, 감사관(코니) 입장에서 보안, 규칙 거버넌스, 리스크 방어 관점의 검토 의견을 제시해 주세요."})
    kony_t3 = call_agent_llm(PERSONAS["kony"], history)
    history.append({"role": "assistant", "content": f"[코니]: {kony_t3}"})
    db_engine.send_message("kony", "all", kony_t3, conversation_id=topic, tier=1)
    asyncio.run(manager.broadcast_live_message({
        "event": "new_message", "sender": "kony", "recipient": "all", "content": kony_t3
    }))

    # Turn 4: Manbok (Final Consensus)
    history.append({"role": "user", "content": "안티와 코니의 의견을 모두 종합하여, 3AI 만장일치 최종 합의안과 향후 구체적 실행 단계를 확정해 주세요."})
    manbok_t4 = call_agent_llm(PERSONAS["manbok"], history)
    history.append({"role": "assistant", "content": f"[만복 합의]: {manbok_t4}"})
    
    final_brief = f"[최종 승인 및 바로보기님 브리핑]\n{manbok_t4}"
    db_engine.send_message("manbok", "all", final_brief, conversation_id=topic, tier=1)
    db_engine.record_decision(
        topic=topic,
        consensus_summary=manbok_t4[:300],
        participants=["manbok", "anti", "kony"],
        approved_by="3AI_live_consensus",
        tier=1
    )
    asyncio.run(manager.broadcast_live_message({
        "event": "new_message", "sender": "manbok", "recipient": "all", "content": final_brief
    }))
    asyncio.run(manager.broadcast_live_message({"event": "debate_finished", "topic": topic}))

@app.post("/api/start_debate")
def start_debate(req: StartDebateRequest, background_tasks: BackgroundTasks):
    threading.Thread(target=_run_real_llm_debate_background, args=(req.topic,), daemon=True).start()
    return {"status": "started", "topic": req.topic}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
