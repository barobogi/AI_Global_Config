"""
3AI Real-Time Hybrid Engine (SQLite WAL + DuckDB Exporter)
Project: 43_function_dev/01_realtime_3ai
Author: Anti (Operator)
"""

import os
import sys
import time
import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SQLITE_PATH = BASE_DIR / "realtime_3ai.db"
DEFAULT_DUCKDB_DIR = BASE_DIR / "snapshots"

class Realtime3AIEngine:
    def __init__(self, db_path: Path = DEFAULT_SQLITE_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA busy_timeout = 5000;")
        return conn

    def _init_db(self):
        schema_path = BASE_DIR / "schema.sql"
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            with self._get_connection() as conn:
                conn.executescript(schema_sql)
                conn.commit()

    def send_message(self, sender: str, recipient: str, content: str, 
                     conversation_id: str = "general", tier: int = 1, metadata: dict = None) -> str:
        """
        Send a real-time message between agents.
        Tier 1: Zero-Human (Internal brainstorm, syntax test)
        Tier 2: Auto-Notified (Refactoring, task state)
        Tier 3: Human-Approved Required (Production, deploy, core rules)
        """
        msg_id = f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        meta_str = json.dumps(metadata or {}, ensure_ascii=False)
        
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO messages (msg_id, conversation_id, sender, recipient, content, tier, status, metadata)
                VALUES (?, ?, ?, ?, ?, ?, 'unread', ?)
                """,
                (msg_id, conversation_id, sender, recipient, content, tier, meta_str)
            )
            conn.commit()
        return msg_id

    def get_unread_messages(self, recipient: str) -> list:
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM messages 
                WHERE (recipient = ? OR recipient = 'all') AND status = 'unread'
                ORDER BY id ASC
                """,
                (recipient,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def mark_message_status(self, msg_id: str, status: str):
        with self._get_connection() as conn:
            conn.execute("UPDATE messages SET status = ? WHERE msg_id = ?", (status, msg_id))
            conn.commit()

    def record_decision(self, topic: str, consensus_summary: str, participants: list, 
                        approved_by: str, tier: int = 1, git_ref: str = None) -> str:
        dec_id = f"dec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        parts_str = json.dumps(participants, ensure_ascii=False)
        
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO decisions (decision_id, topic, consensus_summary, participants, tier, approved_by, git_commit_ref)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (dec_id, topic, consensus_summary, parts_str, tier, approved_by, git_ref)
            )
            conn.commit()
        return dec_id

    def update_heartbeat(self, agent_name: str, status: str = "idle", current_task_id: str = None, sys_info: dict = None):
        info_str = json.dumps(sys_info or {}, ensure_ascii=False)
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO agent_heartbeats (agent_name, status, current_task_id, last_ping, system_info)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)
                ON CONFLICT(agent_name) DO UPDATE SET
                    status=excluded.status,
                    current_task_id=excluded.current_task_id,
                    last_ping=CURRENT_TIMESTAMP,
                    system_info=excluded.system_info
                """,
                (agent_name, status, current_task_id, info_str)
            )
            conn.commit()

    def export_daily_snapshot_to_duckdb(self, export_dir: Path = DEFAULT_DUCKDB_DIR) -> Path:
        """
        Export live SQLite messages & decisions into a DuckDB / Parquet snapshot for Git versioning.
        """
        export_dir.mkdir(parents=True, exist_ok=True)
        today_str = datetime.now().strftime("%Y%m%d")
        snapshot_file = export_dir / f"snapshot_{today_str}.parquet"
        
        # Read from SQLite
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM messages")
            messages_data = [dict(r) for r in cursor.fetchall()]
            
            cursor = conn.execute("SELECT * FROM decisions")
            decisions_data = [dict(r) for r in cursor.fetchall()]

        # Try DuckDB if available, otherwise structured JSON snapshot
        try:
            import duckdb
            duck_db_file = export_dir / f"archive_{today_str}.duckdb"
            con = duckdb.connect(str(duck_db_file))
            con.execute("CREATE OR REPLACE TABLE daily_messages AS SELECT * FROM sqlite_scan(?, 'messages')", (str(self.db_path),))
            con.execute("CREATE OR REPLACE TABLE daily_decisions AS SELECT * FROM sqlite_scan(?, 'decisions')", (str(self.db_path),))
            con.close()
            return duck_db_file
        except Exception:
            # Fallback to structured JSON snapshot
            json_file = export_dir / f"snapshot_{today_str}.json"
            snapshot_payload = {
                "exported_at": datetime.now().isoformat(),
                "messages": messages_data,
                "decisions": decisions_data
            }
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(snapshot_payload, f, ensure_ascii=False, indent=2)
            return json_file

if __name__ == "__main__":
    engine = Realtime3AIEngine()
    print("Initializing 3AI Real-Time Engine...")
    msg_id = engine.send_message("anti", "kony", "Real-time engine self-test", conversation_id="T065_test", tier=1)
    print(f"Sent message ID: {msg_id}")
    unread = engine.get_unread_messages("kony")
    print(f"Unread messages for Kony: {len(unread)}")
    snap = engine.export_daily_snapshot_to_duckdb()
    print(f"Exported snapshot to: {snap}")
