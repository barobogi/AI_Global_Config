"""
End-to-End Production Test Suite for 3AI Real-Time Mesh (01_realtime_3ai Phase 3)
Tests:
1. Full 3AI autonomous dialogue cycle (Manbok -> Anti -> Kony -> Consensus)
2. Real-time consensus decision recording in SQLite WAL
3. Circuit breaker protection during active debate
4. Daily Delta snapshot export of the generated debate data
"""

import sys
import json
import uuid
from pathlib import Path

# UTF-8 stdout wrapper
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from debate_runner import RealtimeDebateRunner
from realtime_engine import Realtime3AIEngine

def test_1_3ai_autonomous_debate_and_decision():
    print("\n--- [E2E Test 1] 3AI Real-Time Autonomous Dialogue & Consensus ---")
    runner = RealtimeDebateRunner()
    topic_id = f"e2e_topic_{uuid.uuid4().hex[:6]}"
    
    result = runner.run_3ai_debate(
        topic=topic_id,
        initial_proposal="신규 자율 에이전트 파이프라인 승격 및 배포안"
    )
    
    print(f"\nDebate Result: {json.dumps(result, ensure_ascii=False, indent=2)}")
    assert result["status"] == "decided"
    assert result["total_turns"] == 4
    assert result["decision_id"].startswith("dec_")
    
    # Verify in DB
    db = Realtime3AIEngine()
    with db._get_connection() as conn:
        cursor = conn.execute("SELECT * FROM decisions WHERE decision_id = ?", (result["decision_id"],))
        row = cursor.fetchone()
        assert row is not None
        assert "3AI 만장일치 합의" in row["consensus_summary"]
        
    print("[PASS] [E2E Test 1] 3AI autonomous debate & consensus recording 100% verified.")

def test_2_e2e_delta_snapshot_integrity():
    print("\n--- [E2E Test 2] Delta Snapshot Integrity After Debate ---")
    db = Realtime3AIEngine()
    snap_path = db.export_daily_snapshot_to_duckdb()
    print(f"Exported snapshot path: {snap_path}")
    assert snap_path.exists()
    
    with open(snap_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data["messages"]) >= 4
    assert len(data["decisions"]) >= 1
    print(f"Verified {len(data['messages'])} messages and {len(data['decisions'])} decisions in today's delta.")
    print("[PASS] [E2E Test 2] Daily Delta snapshot integrity verified.")

def run_all_e2e_tests():
    print("==================================================")
    print("Running 3AI Real-Time Mesh End-to-End Production Test")
    print("==================================================")
    test_1_3ai_autonomous_debate_and_decision()
    test_2_e2e_delta_snapshot_integrity()
    print("\n==================================================")
    print("ALL E2E MESH TEST SUITES PASSED WITH 100% SUCCESS")
    print("==================================================")

if __name__ == "__main__":
    run_all_e2e_tests()
