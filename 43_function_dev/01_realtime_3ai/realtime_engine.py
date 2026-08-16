"""
3AI Real-Time Hybrid Engine (SQLite WAL + DuckDB Daily Delta Exporter + Circuit Breaker)
Project: 43_function_dev/01_realtime_3ai
Author: Anti (Operator)
"""

import os
import sys
import time
import json
import sqlite3
import uuid
from datetime import datetime, date
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SQLITE_PATH = BASE_DIR / "realtime_3ai.db"
DEFAULT_DUCKDB_DIR = BASE_DIR / "snapshots"

class CircuitBreakerOpenError(Exception):
    """Raised when an agent conversation exceeds maximum turn limits without consensus."""
    pass

class ImpersonationSecurityError(Exception):
    """Raised when an unauthorized script attempts to forge or record actions on behalf of another AI."""
    pass

# Authenticated session tokens for 3AI identity provenance
AGENT_SESSION_TOKENS = {
    "manbok": os.environ.get("MANBOK_SESSION_TOKEN", "token_manbok_session_auth"),
    "kony": os.environ.get("KONY_SESSION_TOKEN", "token_kony_session_auth"),
    "anti": os.environ.get("ANTI_SESSION_TOKEN", "token_anti_session_auth"),
    "system": "token_system_internal"
}

class Realtime3AIEngine:
    MAX_TURNS_DEFAULT = 5

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

    def get_conversation_turn_count(self, conversation_id: str) -> int:
        """Count the number of non-system dialogue turns in a conversation."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT COUNT(*) as cnt FROM messages 
                WHERE conversation_id = ? AND sender IN ('manbok', 'kony', 'anti')
                """,
                (conversation_id,)
            )
            row = cursor.fetchone()
            return row["cnt"] if row else 0

    def is_conversation_decided(self, conversation_id: str) -> bool:
        """Check if a decision/consensus has already been recorded for this topic."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) as cnt FROM decisions WHERE topic = ?",
                (conversation_id,)
            )
            row = cursor.fetchone()
            return (row["cnt"] > 0) if row else False

    def send_message(self, sender: str, recipient: str, content: str, 
                     conversation_id: str = "general", tier: int = 1, 
                     metadata: dict = None, max_turns: int = MAX_TURNS_DEFAULT) -> str:
        """
        Send a real-time message between agents with Circuit Breaker protection.
        Tier 1: Zero-Human (Internal brainstorm, syntax test) - Hard Cap 5 turns
        Tier 2: Auto-Notified (Refactoring, task state)
        Tier 3: Human-Approved Required (Production, deploy, core rules)
        """
        # Circuit Breaker Check (for Tier 1 internal dialogue)
        if tier == 1 and conversation_id != "general":
            current_turns = self.get_conversation_turn_count(conversation_id)
            if current_turns >= max_turns and not self.is_conversation_decided(conversation_id):
                # Mark conversation as escalated in messages
                esc_msg_id = f"esc_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
                with self._get_connection() as conn:
                    conn.execute(
                        """
                        INSERT INTO messages (msg_id, conversation_id, sender, recipient, content, tier, status, metadata)
                        VALUES (?, ?, 'system', 'all', ?, 1, 'escalated', ?)
                        """,
                        (esc_msg_id, conversation_id, 
                         f"[Circuit Breaker Tripped] 대화 {conversation_id}가 {max_turns}턴 내 합의에 도달하지 못해 강제 중단되었습니다.",
                         json.dumps({"reason": "max_turns_exceeded", "turns": current_turns}))
                    )
                    conn.commit()
                raise CircuitBreakerOpenError(
                    f"Circuit Breaker Tripped: Conversation '{conversation_id}' exceeded {max_turns} turns without consensus."
                )

        msg_id = f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        meta_str = json.dumps(metadata or {}, ensure_ascii=False)
        local_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO messages (msg_id, conversation_id, sender, recipient, content, tier, status, metadata, created_at)
                VALUES (?, ?, ?, ?, ?, ?, 'unread', ?, ?)
                """,
                (msg_id, conversation_id, sender, recipient, content, tier, meta_str, local_time_str)
            )
            conn.commit()

        # Trigger popup notification over MCP bridge (port 5003)
        if recipient in ("manbok", "kony") and sender != recipient:
            self._dispatch_popup_trigger(recipient)
        elif recipient == "all" and sender not in ("system", "test_runner"):
            for r in ("manbok", "kony"):
                if r != sender:
                    self._dispatch_popup_trigger(r)

        return msg_id

    def _dispatch_popup_trigger(self, target: str):
        """Asynchronously notify mcp_server on port 5003 when a new message is inserted."""
        def _post():
            try:
                import urllib.request
                url = "http://127.0.0.1:5003/trigger"
                payload = json.dumps({"target": target}).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
                with urllib.request.urlopen(req, timeout=2.0) as resp:
                    pass
            except Exception:
                pass
        import threading
        t = threading.Thread(target=_post, daemon=True)
        t.start()

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

    def record_decision(self, topic: str, consensus_summary: str, 
                        participants: list, approved_by: str, tier: int = 1,
                        git_ref: str = None, auth_token: str = None) -> str:
        """
        Record final consensus decision into SQLite WAL.
        Enforces security provenance: 'approved_by' must provide matching auth_token.
        """
        # Provenance verification gate
        if approved_by in AGENT_SESSION_TOKENS:
            expected_token = AGENT_SESSION_TOKENS[approved_by]
            if auth_token != expected_token and os.environ.get("ENFORCE_PROVENANCE_AUTH", "1") == "1":
                raise ImpersonationSecurityError(
                    f"[Security Gate] Impersonation blocked: Cannot sign decision as '{approved_by}' without valid session token."
                )

        dec_id = f"dec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO decisions (decision_id, topic, consensus_summary, participants, approved_by, tier, git_commit_ref)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (dec_id, topic, consensus_summary, json.dumps(participants, ensure_ascii=False), approved_by, tier, git_ref)
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

    def export_daily_snapshot_to_duckdb(self, target_date: str = None, export_dir: Path = DEFAULT_DUCKDB_DIR) -> Path:
        """
        Export ONLY the delta (rows created on target_date) into a DuckDB / Parquet snapshot.
        This ensures each daily snapshot file is an independent, non-bloating daily delta.
        target_date: YYYY-MM-DD or YYYYMMDD format. Default is today.
        """
        export_dir.mkdir(parents=True, exist_ok=True)
        if not target_date:
            target_date = datetime.now().strftime("%Y-%m-%d")
        else:
            # Normalize target_date to YYYY-MM-DD
            target_date = target_date.replace("_", "-")
            if len(target_date) == 8:
                target_date = f"{target_date[:4]}-{target_date[4:6]}-{target_date[6:]}"

        date_compact = target_date.replace("-", "")
        
        # Read ONLY today's delta from SQLite
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM messages WHERE DATE(created_at) = DATE(?)",
                (target_date,)
            )
            messages_delta = [dict(r) for r in cursor.fetchall()]
            
            cursor = conn.execute(
                "SELECT * FROM decisions WHERE DATE(created_at) = DATE(?)",
                (target_date,)
            )
            decisions_delta = [dict(r) for r in cursor.fetchall()]

        # Try DuckDB if available, otherwise structured JSON snapshot
        try:
            import duckdb
            duck_db_file = export_dir / f"delta_{date_compact}.duckdb"
            con = duckdb.connect(str(duck_db_file))
            con.execute(
                "CREATE OR REPLACE TABLE daily_messages AS SELECT * FROM sqlite_scan(?, 'messages') WHERE strftime(created_at, '%Y-%m-%d') = ?",
                (str(self.db_path), target_date)
            )
            con.execute(
                "CREATE OR REPLACE TABLE daily_decisions AS SELECT * FROM sqlite_scan(?, 'decisions') WHERE strftime(created_at, '%Y-%m-%d') = ?",
                (str(self.db_path), target_date)
            )
            con.close()
            return duck_db_file
        except Exception:
            json_file = export_dir / f"delta_{date_compact}.json"
            snapshot_payload = {
                "snapshot_date": target_date,
                "exported_at": datetime.now().isoformat(),
                "row_counts": {
                    "messages": len(messages_delta),
                    "decisions": len(decisions_delta)
                },
                "messages": messages_delta,
                "decisions": decisions_delta
            }
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(snapshot_payload, f, ensure_ascii=False, indent=2)
            return json_file
