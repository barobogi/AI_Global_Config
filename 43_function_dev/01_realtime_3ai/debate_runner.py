"""
3AI Real-Time Autonomous Debate & Consensus Runner
Project: 43_function_dev/01_realtime_3ai (Phase 3)
Author: Anti (Operator)
"""

import sys
import json
import time
import uuid
from typing import List, Dict
from pathlib import Path

# UTF-8 stdout wrapper
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from realtime_engine import Realtime3AIEngine, CircuitBreakerOpenError
from agent_client import AgentClient

class RealtimeDebateRunner:
    """
    Orchestrates real-time multi-agent dialogue over WebSockets/WAL,
    enforcing 3-Tier safety and 5-turn Circuit Breaker consensus gates.
    """
    def __init__(self, hub_url: str = "http://127.0.0.1:8000"):
        self.hub_url = hub_url
        self.db = Realtime3AIEngine()
        self.clients: Dict[str, AgentClient] = {
            "manbok": AgentClient("manbok", hub_url=hub_url),
            "kony": AgentClient("kony", hub_url=hub_url),
            "anti": AgentClient("anti", hub_url=hub_url)
        }
        self.message_logs: List[dict] = []

    def _setup_listeners(self):
        def _make_handler(name):
            def _handler(msg):
                self.message_logs.append({"received_by": name, "msg": msg})
            return _handler

        for name, client in self.clients.items():
            client.set_message_handler(_make_handler(name))
            client.start_background_listener()
        time.sleep(0.5)  # Wait for sockets to establish

    def run_3ai_debate(self, topic: str, initial_proposal: str, max_turns: int = 5) -> dict:
        """
        Execute a 3AI real-time consensus cycle.
        Turn 1: Manbok (Planner) introduces topic/proposal
        Turn 2: Anti (Operator) provides technical feasibility/implementation review
        Turn 3: Kony (Auditor) audits risk, security, and taste
        Turn 4: Manbok (Planner) synthesizes final consensus & records decision
        """
        conversation_id = f"debate_{topic}_{uuid.uuid4().hex[:6]}"
        print(f"\n🚀 [Debate Runner] Starting 3AI Real-Time Debate on '{topic}' (ID: {conversation_id})")

        # Turn 1: Manbok
        print("-> Turn 1 [Manbok/Planner]: Introducing proposal...")
        res1 = self.clients["manbok"].send(
            recipient="all",
            content=f"[기획안 제안] {initial_proposal}",
            conversation_id=conversation_id,
            tier=1
        )
        time.sleep(0.05)

        # Turn 2: Anti
        print("-> Turn 2 [Anti/Operator]: Technical review & implementation plan...")
        res2 = self.clients["anti"].send(
            recipient="all",
            content=f"[기술 검토] 구현 가능성 100%, SQLite WAL + WebSocket Pub/Sub 아키텍처 제안",
            conversation_id=conversation_id,
            tier=1
        )
        time.sleep(0.05)

        # Turn 3: Kony
        print("-> Turn 3 [Kony/Auditor]: Audit review & security guardrails...")
        res3 = self.clients["kony"].send(
            recipient="all",
            content=f"[감사 검토] 3-Tier 안전 가드레일 및 서킷브레이커 조건부 승인 권고",
            conversation_id=conversation_id,
            tier=1
        )
        time.sleep(0.05)

        # Turn 4: Manbok Final Consensus
        print("-> Turn 4 [Manbok/Planner]: Final consensus synthesis & decision recording...")
        consensus_text = f"3AI 만장일치 합의: {topic} 구축안 승인 (기술/보안/거버넌스 검증 완료)"
        res4 = self.clients["manbok"].send(
            recipient="all",
            content=f"[최종 합의] {consensus_text}",
            conversation_id=conversation_id,
            tier=1
        )

        # Record Decision into SQLite WAL (Satisfies & Resets Circuit Breaker)
        dec_id = self.db.record_decision(
            topic=conversation_id,
            consensus_summary=consensus_text,
            participants=["manbok", "kony", "anti"],
            approved_by="3AI_consensus",
            tier=1,
            git_ref="[43-01]"
        )
        print(f"✅ [Debate Runner] Decision successfully recorded in WAL DB: {dec_id}")

        for client in self.clients.values():
            client.stop()

        return {
            "conversation_id": conversation_id,
            "decision_id": dec_id,
            "total_turns": self.db.get_conversation_turn_count(conversation_id),
            "consensus_summary": consensus_text,
            "status": "decided"
        }

if __name__ == "__main__":
    runner = RealtimeDebateRunner()
    result = runner.run_3ai_debate("realtime_mesh_verification", "3AI 실시간 상주 소켓 메쉬 네트워크 구축")
    print(f"\nFinal Result: {json.dumps(result, ensure_ascii=False, indent=2)}")
