"""
3AI Real-Time Agent Client (WebSocket + REST Fallback)
Project: 43_function_dev/01_realtime_3ai
Author: Anti (Operator)
"""

import sys
import json
import asyncio
import threading
from typing import Callable, Optional
from pathlib import Path
import websockets
import requests

# UTF-8 stdout wrapper
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from realtime_engine import Realtime3AIEngine

class AgentClient:
    def __init__(self, agent_name: str, hub_url: str = "http://127.0.0.1:8000", 
                 ws_url: str = "ws://127.0.0.1:8000"):
        self.agent_name = agent_name
        self.hub_url = hub_url
        self.ws_url = f"{ws_url}/ws/{agent_name}"
        self.local_db = Realtime3AIEngine()
        self.on_message_callback: Optional[Callable] = None
        self._ws_task = None
        self._running = False

    def set_message_handler(self, callback: Callable[[dict], None]):
        """Register a callback function when a new live message arrives."""
        self.on_message_callback = callback

    def send(self, recipient: str, content: str, conversation_id: str = "general", 
             tier: int = 1, metadata: dict = None) -> dict:
        """Send message via Hub HTTP API, with direct SQLite WAL fallback."""
        payload = {
            "sender": self.agent_name,
            "recipient": recipient,
            "content": content,
            "conversation_id": conversation_id,
            "tier": tier,
            "metadata": metadata or {}
        }
        try:
            res = requests.post(f"{self.hub_url}/send", json=payload, timeout=2.0)
            if res.status_code == 200:
                return res.json()
            elif res.status_code == 429:
                return {"status": "error", "type": "circuit_breaker_tripped", "detail": res.text}
        except Exception:
            # Fallback directly to SQLite WAL
            pass

        # SQLite Direct Fallback
        msg_id = self.local_db.send_message(
            sender=self.agent_name,
            recipient=recipient,
            content=content,
            conversation_id=conversation_id,
            tier=tier,
            metadata=metadata
        )
        return {"status": "success", "msg_id": msg_id, "fallback": True}

    async def _listen_loop(self):
        while self._running:
            try:
                async with websockets.connect(self.ws_url) as ws:
                    print(f"[{self.agent_name}] Connected to Real-Time Hub WebSocket.")
                    while self._running:
                        msg_raw = await ws.recv()
                        data = json.loads(msg_raw)
                        if self.on_message_callback:
                            self.on_message_callback(data)
            except Exception:
                await asyncio.sleep(2.0)

    def start_background_listener(self):
        """Start background WebSocket listener thread."""
        self._running = True
        
        def _runner():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._listen_loop())
            
        t = threading.Thread(target=_runner, daemon=True)
        t.start()
        return t

    def stop(self):
        self._running = False
