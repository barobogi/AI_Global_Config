"""
3AI Spool/Outbox Relay Watcher
Project: 43_function_dev/01_realtime_3ai
Author: Manbok (built directly per 안티's root-cause diagnosis: SQLite WAL mode
requires all writers to share the same machine's -shm file; a network-mounted
session (kony) can never safely write SQLite WAL directly - per SQLite's own
docs this causes silent data loss/inconsistency across network filesystems.

This watcher lets kony avoid SQLite entirely for WRITES: she drops a plain
JSON file into spool/ (a plain file write IS safe over a network mount,
unlike WAL), and this script - running natively on the Windows host, no
network mount involved - performs the actual local SQLite INSERT on her
behalf via the existing send_message() provenance-checked API.

It also solves the matching READ-side problem (2026-08-17): kony was still
querying realtime_3ai.db directly to read messages, which occasionally hit
"database is locked" against her own EXCLUSIVE-mode connection racing other
writers. Each loop iteration this script also dumps a plain JSON snapshot of
the latest messages to latest_snapshot.json - kony reads that file instead of
ever opening the SQLite file herself, for both reading and writing.
"""

import sys
import json
import time
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
from realtime_engine import Realtime3AIEngine, ImpersonationSecurityError

SPOOL_DIR = BASE_DIR / "spool"
FAILED_DIR = SPOOL_DIR / "_failed"
SPOOL_DIR.mkdir(exist_ok=True)
FAILED_DIR.mkdir(exist_ok=True)

SNAPSHOT_PATH = BASE_DIR / "latest_snapshot.json"
SNAPSHOT_TMP_PATH = BASE_DIR / "latest_snapshot.json.tmp"
SNAPSHOT_MESSAGE_COUNT = 50


def process_spool_file(engine: Realtime3AIEngine, path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for required_field in ("sender", "recipient", "content"):
            if required_field not in data:
                raise ValueError(f"missing required field: {required_field}")

        msg_id = engine.send_message(
            sender=data["sender"],
            recipient=data["recipient"],
            content=data["content"],
            conversation_id=data.get("conversation_id", "general"),
            tier=int(data.get("tier", 1)),
            metadata=data.get("metadata"),
            auth_token=data.get("auth_token"),
        )
        print(f"[spool_watcher] relayed {path.name} -> msg_id={msg_id}", flush=True)
        path.unlink()
    except ImpersonationSecurityError as e:
        print(f"[spool_watcher] BLOCKED (impersonation) {path.name}: {e}", flush=True)
        path.rename(FAILED_DIR / path.name)
    except Exception as e:
        print(f"[spool_watcher] FAILED {path.name}: {e}", flush=True)
        try:
            path.rename(FAILED_DIR / path.name)
        except Exception:
            pass


def export_snapshot(engine: Realtime3AIEngine):
    """Write the latest messages to a plain JSON file (atomic write-then-rename)
    so kony can read chat state without ever opening the SQLite file herself."""
    try:
        with engine._get_connection() as conn:
            rows = conn.execute(
                "SELECT id, msg_id, sender, recipient, conversation_id, content, "
                "tier, status, created_at FROM messages ORDER BY id DESC LIMIT ?",
                (SNAPSHOT_MESSAGE_COUNT,),
            ).fetchall()
        payload = {
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "messages": [dict(r) for r in reversed(rows)],
        }
        with open(SNAPSHOT_TMP_PATH, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        SNAPSHOT_TMP_PATH.replace(SNAPSHOT_PATH)  # atomic on the same filesystem
    except Exception as e:
        print(f"[spool_watcher] snapshot export failed: {e}", flush=True)


def run(poll_interval: float = 1.0):
    engine = Realtime3AIEngine()
    print(f"[spool_watcher] watching {SPOOL_DIR} every {poll_interval}s", flush=True)
    while True:
        for path in sorted(SPOOL_DIR.glob("*.json")):
            process_spool_file(engine, path)
        export_snapshot(engine)
        time.sleep(poll_interval)


if __name__ == "__main__":
    run()
