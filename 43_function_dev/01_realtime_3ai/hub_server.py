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
    auth_token: str = None

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
            "SELECT * FROM messages ORDER BY id DESC LIMIT ?", (limit,)
        )
        rows = [dict(r) for r in cursor.fetchall()]
        rows.reverse()
        return {"messages": rows}

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
                auth_token = msg_payload.get("auth_token")
                
                msg_id = db_engine.send_message(
                    sender=sender,
                    recipient=recipient,
                    content=content,
                    conversation_id=conversation_id,
                    tier=tier,
                    auth_token=auth_token
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
            metadata=req.metadata,
            auth_token=req.auth_token
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
