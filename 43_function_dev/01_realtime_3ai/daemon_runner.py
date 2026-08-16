"""
3AI Real-Time Daemon Runner
Project: 43_function_dev/01_realtime_3ai
Author: Anti (Operator)
"""

import sys
import time
import argparse
from pathlib import Path

# UTF-8 stdout wrapper
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from agent_client import AgentClient
from realtime_engine import Realtime3AIEngine

def run_agent_daemon(agent_name: str, hub_url: str = "http://127.0.0.1:8000"):
    print(f"==================================================")
    print(f"🤖 Starting 3AI Real-Time Daemon: [{agent_name.upper()}]")
    print(f"Hub URL: {hub_url}")
    print(f"==================================================")
    
    db = Realtime3AIEngine()
    db.update_heartbeat(agent_name, status="online", sys_info={"daemon": "running"})
    
    client = AgentClient(agent_name, hub_url=hub_url)
    
    def on_message_received(msg_payload):
        event = msg_payload.get("event")
        sender = msg_payload.get("sender")
        content = msg_payload.get("content")
        print(f"\n⚡ [{agent_name.upper()} INCOMING LIVE MESSAGE]")
        print(f"From: {sender} | Content: {content}")
        
    client.set_message_handler(on_message_received)
    client.start_background_listener()
    
    print(f"[{agent_name.upper()}] Background listener active. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1.0)
            db.update_heartbeat(agent_name, status="idle")
    except KeyboardInterrupt:
        print(f"\n[{agent_name.upper()}] Shutting down daemon...")
        client.stop()
        db.update_heartbeat(agent_name, status="offline")
        print("Daemon stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="3AI Real-Time Agent Daemon")
    parser.add_argument("--agent", type=str, default="anti", choices=["manbok", "kony", "anti", "human"])
    parser.add_argument("--hub", type=str, default="http://127.0.0.1:8000")
    args = parser.parse_args()
    
    run_agent_daemon(agent_name=args.agent, hub_url=args.hub)
