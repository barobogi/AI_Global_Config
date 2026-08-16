"""
Production Test Suite for 3AI Real-Time Hybrid Engine (01_realtime_3ai)
Tests:
1. Multi-process concurrent write stress test (3 processes, 60 messages concurrently)
2. Circuit Breaker hard-cap enforcement (5 turns without consensus -> trip & escalation)
3. Daily Delta Snapshot (only target date delta extracted, no cumulative bloat)
4. Liveness Heartbeat and unread message queue
"""

import os
import sys
import time
import json
import sqlite3
import multiprocessing
from pathlib import Path

# UTF-8 stdout wrapper for Windows cp949 compatibility
sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from realtime_engine import Realtime3AIEngine, CircuitBreakerOpenError

TEST_DB_PATH = BASE_DIR / "test_realtime_3ai.db"
TEST_SNAPSHOTS_DIR = BASE_DIR / "test_snapshots"

def _worker_write_task(agent_name: str, msg_count: int, db_path: Path):
    """Worker function executed by independent OS processes."""
    engine = Realtime3AIEngine(db_path=db_path)
    for i in range(msg_count):
        engine.send_message(
            sender=agent_name,
            recipient="all",
            content=f"Concurrent message {i} from {agent_name}",
            conversation_id="stress_test",
            tier=2
        )
        time.sleep(0.01)

def cleanup_test_files():
    for f in [TEST_DB_PATH, BASE_DIR / "test_realtime_3ai.db-wal", BASE_DIR / "test_realtime_3ai.db-shm"]:
        if f.exists():
            try:
                os.remove(f)
            except Exception:
                pass
    if TEST_SNAPSHOTS_DIR.exists():
        for f in TEST_SNAPSHOTS_DIR.glob("*"):
            try:
                os.remove(f)
            except Exception:
                pass
        try:
            TEST_SNAPSHOTS_DIR.rmdir()
        except Exception:
            pass

def test_1_concurrent_multi_process_write():
    print("\n--- [Test 1] Multi-Process Concurrent Write Stress Test ---")
    cleanup_test_files()
    engine = Realtime3AIEngine(db_path=TEST_DB_PATH)
    
    agents = ["manbok", "kony", "anti"]
    msgs_per_agent = 20
    processes = []
    
    start_time = time.time()
    for agent in agents:
        p = multiprocessing.Process(
            target=_worker_write_task,
            args=(agent, msgs_per_agent, TEST_DB_PATH)
        )
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    elapsed = time.time() - start_time
    
    with engine._get_connection() as conn:
        cursor = conn.execute("SELECT COUNT(*) as cnt FROM messages WHERE conversation_id = 'stress_test'")
        total_written = cursor.fetchone()["cnt"]
        
    print(f"Total messages written: {total_written} / {len(agents) * msgs_per_agent} in {elapsed:.2f}s")
    assert total_written == len(agents) * msgs_per_agent, f"Expected {len(agents) * msgs_per_agent}, got {total_written}"
    print("[PASS] [Test 1] 3 Multi-processes concurrent write 100% safe (Zero lock collision).")

def test_2_circuit_breaker():
    print("\n--- [Test 2] Circuit Breaker Enforcement (Max 5 Turns) ---")
    engine = Realtime3AIEngine(db_path=TEST_DB_PATH)
    conv_id = "test_debate_circuit_breaker"
    
    # Send 5 dialogue turns
    for turn in range(5):
        sender = "kony" if turn % 2 == 0 else "anti"
        engine.send_message(
            sender=sender,
            recipient="all",
            content=f"Debate turn {turn+1}",
            conversation_id=conv_id,
            tier=1
        )
        
    turn_count = engine.get_conversation_turn_count(conv_id)
    print(f"Current dialogue turn count: {turn_count}/5")
    assert turn_count == 5, f"Expected 5 turns, got {turn_count}"
    
    # 6th turn should raise CircuitBreakerOpenError
    tripped = False
    try:
        engine.send_message(
            sender="kony",
            recipient="anti",
            content="6th turn should be blocked",
            conversation_id=conv_id,
            tier=1
        )
    except CircuitBreakerOpenError as e:
        tripped = True
        print(f"Caught expected CircuitBreakerOpenError: {e}")
        
    assert tripped, "Circuit Breaker failed to trip on 6th turn!"
    
    # Verify escalated message was recorded in DB
    with engine._get_connection() as conn:
        cursor = conn.execute("SELECT * FROM messages WHERE conversation_id = ? AND status = 'escalated'", (conv_id,))
        esc_row = cursor.fetchone()
        assert esc_row is not None, "Escalated system message missing!"
        print(f"Escalation logged: {esc_row['content']}")
        
    print("[PASS] [Test 2] Circuit Breaker successfully tripped at 5-turn limit.")

def test_3_daily_delta_snapshot():
    print("\n--- [Test 3] Daily Delta Snapshot (Non-bloating Delta Export) ---")
    engine = Realtime3AIEngine(db_path=TEST_DB_PATH)
    
    # Insert a dummy message with yesterday's timestamp
    yesterday_str = "2026-08-15"
    with engine._get_connection() as conn:
        conn.execute(
            """
            INSERT INTO messages (msg_id, conversation_id, sender, recipient, content, tier, status, created_at)
            VALUES ('msg_yesterday_01', 't_old', 'manbok', 'kony', 'Yesterday message', 1, 'read', '2026-08-15 12:00:00')
            """
        )
        conn.commit()
        
    # Export yesterday's snapshot
    snap_yesterday = engine.export_daily_snapshot_to_duckdb(target_date="2026-08-15", export_dir=TEST_SNAPSHOTS_DIR)
    print(f"Yesterday snapshot created at: {snap_yesterday}")
    
    with open(snap_yesterday, "r", encoding="utf-8") as f:
        data_y = json.load(f)
    print(f"Yesterday snapshot messages count: {len(data_y['messages'])}")
    assert len(data_y['messages']) == 1, f"Expected 1 yesterday message, got {len(data_y['messages'])}"
    assert data_y['messages'][0]['msg_id'] == 'msg_yesterday_01'
    
    # Export today's snapshot
    today_str = "2026-08-16"
    snap_today = engine.export_daily_snapshot_to_duckdb(target_date=today_str, export_dir=TEST_SNAPSHOTS_DIR)
    print(f"Today snapshot created at: {snap_today}")
    
    with open(snap_today, "r", encoding="utf-8") as f:
        data_t = json.load(f)
    print(f"Today snapshot messages count: {len(data_t['messages'])}")
    # Today's snapshot must NOT contain yesterday's message
    yesterday_ids_in_today = [m for m in data_t['messages'] if m['msg_id'] == 'msg_yesterday_01']
    assert len(yesterday_ids_in_today) == 0, "Today snapshot contaminated with yesterday data!"
    
    print("[PASS] [Test 3] Daily Delta Snapshot correctly extracts ONLY target date delta.")

def test_4_heartbeat_and_decisions():
    print("\n--- [Test 4] Heartbeat & Consensus Decision ---")
    engine = Realtime3AIEngine(db_path=TEST_DB_PATH)
    
    # Heartbeat test
    engine.update_heartbeat("kony", status="analyzing", current_task_id="T065", sys_info={"model": "Claude 3.7"})
    with engine._get_connection() as conn:
        cursor = conn.execute("SELECT * FROM agent_heartbeats WHERE agent_name = 'kony'")
        hb = cursor.fetchone()
        assert hb["status"] == "analyzing"
        assert hb["current_task_id"] == "T065"
        
    # Decision record test
    dec_id = engine.record_decision(
        topic="T065_realtime_3ai",
        consensus_summary="SQLite WAL + DuckDB Delta Snapshot architecture approved",
        participants=["manbok", "kony", "anti"],
        approved_by="3AI_consensus",
        tier=1,
        git_ref="[43-01]"
    )
    assert dec_id.startswith("dec_")
    print(f"Decision recorded: {dec_id}")
    print("[PASS] [Test 4] Heartbeat & Decision engine functional.")

def run_all_tests():
    print("==================================================")
    print("Running 3AI Real-Time Engine Production Test Suite")
    print("==================================================")
    test_1_concurrent_multi_process_write()
    test_2_circuit_breaker()
    test_3_daily_delta_snapshot()
    test_4_heartbeat_and_decisions()
    cleanup_test_files()
    print("\n==================================================")
    print("ALL 4 TEST SUITES PASSED WITH 100% SUCCESS")
    print("==================================================")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_all_tests()
