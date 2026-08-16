"""
3AI Real-Time Local Pub/Sub Hub Server (FastAPI + WebSockets)
Project: 43_function_dev/01_realtime_3ai (Phase 2)
Author: Anti (Operator)
"""

import sys
import json
import asyncio
from typing import Dict, List
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# UTF-8 stdout wrapper
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from realtime_engine import Realtime3AIEngine, CircuitBreakerOpenError

# Initialize Database Engine
db_engine = Realtime3AIEngine()

class ConnectionManager:
    def __init__(self):
        # Active connections: agent_name -> List[WebSocket]
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
        print(f"[Hub] Agent '{agent_name}' connected. (Active: {len(self.active_connections[agent_name])})")

    def disconnect(self, websocket: WebSocket, agent_name: str):
        if agent_name in self.active_connections and websocket in self.active_connections[agent_name]:
            self.active_connections[agent_name].remove(websocket)
            if not self.active_connections[agent_name]:
                db_engine.update_heartbeat(agent_name, status="offline")
            print(f"[Hub] Agent '{agent_name}' disconnected.")

    async def send_direct_message(self, recipient: str, payload: dict) -> bool:
        """Push instant message to connected recipient WebSocket (<5ms)."""
        delivered = False
        if recipient == "all":
            for name, sockets in self.active_connections.items():
                for ws in sockets:
                    try:
                        await ws.send_json(payload)
                        delivered = True
                    except Exception:
                        pass
        elif recipient in self.active_connections:
            for ws in self.active_connections[recipient]:
                try:
                    await ws.send_json(payload)
                    delivered = True
                except Exception:
                    pass
        return delivered

manager = ConnectionManager()

# Request Models
class SendMessageRequest(BaseModel):
    sender: str
    recipient: str
    content: str
    conversation_id: str = "general"
    tier: int = 1
    metadata: dict = None

class RecordDecisionRequest(BaseModel):
    topic: str
    consensus_summary: str
    participants: List[str]
    approved_by: str = "3AI_consensus"
    tier: int = 1
    git_ref: str = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[Hub] 3AI Real-Time Pub/Sub Hub Server Started on port 8000.")
    yield
    print("[Hub] 3AI Real-Time Pub/Sub Hub Server Stopped.")

app = FastAPI(
    title="3AI Real-Time Pub/Sub Hub",
    version="1.0.0",
    description="Low-latency (<5ms) multi-agent WebSocket broker & SQLite WAL persistence layer",
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"status": "running", "service": "3AI Real-Time Pub/Sub Hub"}

@app.websocket("/ws/{agent_name}")
async def websocket_endpoint(websocket: WebSocket, agent_name: str):
    await manager.connect(websocket, agent_name)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg_payload = json.loads(data)
                # Handle incoming socket message
                sender = agent_name
                recipient = msg_payload.get("recipient", "all")
                content = msg_payload.get("content", "")
                conversation_id = msg_payload.get("conversation_id", "general")
                tier = int(msg_payload.get("tier", 1))
                
                # Persist to SQLite WAL with Circuit Breaker
                msg_id = db_engine.send_message(
                    sender=sender,
                    recipient=recipient,
                    content=content,
                    conversation_id=conversation_id,
                    tier=tier,
                    metadata=msg_payload.get("metadata")
                )
                
                # Push instantly to recipient
                out_payload = {
                    "event": "new_message",
                    "msg_id": msg_id,
                    "sender": sender,
                    "recipient": recipient,
                    "content": content,
                    "conversation_id": conversation_id,
                    "tier": tier
                }
                await manager.send_direct_message(recipient, out_payload)
            except CircuitBreakerOpenError as cbe:
                await websocket.send_json({
                    "event": "error",
                    "type": "circuit_breaker_tripped",
                    "detail": str(cbe)
                })
            except Exception as e:
                await websocket.send_json({
                    "event": "error",
                    "detail": str(e)
                })
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
        # Push to live WebSocket subscribers
        out_payload = {
            "event": "new_message",
            "msg_id": msg_id,
            "sender": req.sender,
            "recipient": req.recipient,
            "content": req.content,
            "conversation_id": req.conversation_id,
            "tier": req.tier
        }
        delivered_live = await manager.send_direct_message(req.recipient, out_payload)
        return {
            "status": "success",
            "msg_id": msg_id,
            "live_delivered": delivered_live
        }
    except CircuitBreakerOpenError as cbe:
        raise HTTPException(status_code=429, detail=str(cbe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/unread/{agent_name}")
def get_unread(agent_name: str):
    unread = db_engine.get_unread_messages(agent_name)
    return {"agent_name": agent_name, "count": len(unread), "messages": unread}

@app.post("/decisions")
def record_decision(req: RecordDecisionRequest):
    dec_id = db_engine.record_decision(
        topic=req.topic,
        consensus_summary=req.consensus_summary,
        participants=req.participants,
        approved_by=req.approved_by,
        tier=req.tier,
        git_ref=req.git_ref
    )
    return {"status": "success", "decision_id": dec_id}

@app.get("/export_snapshot")
def export_snapshot(date_str: str = None):
    snap_path = db_engine.export_daily_snapshot_to_duckdb(target_date=date_str)
    return {"status": "success", "snapshot_path": str(snap_path)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
