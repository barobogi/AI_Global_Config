"""
3AI Spool/Outbox Relay Watcher
Project: 43_function_dev/01_realtime_3ai
Author: Manbok (built directly per 안티's root-cause diagnosis: SQLite WAL mode
requires all writers to share the same machine's -shm file; a network-mounted
session (kony) can never safely write SQLite WAL directly - per SQLite's own
docs this causes silent data loss/inconsistency across network filesystems.

This watcher lets kony avoid SQLite entirely: she drops a plain JSON file into
spool/ (a plain file write IS safe over a network mount, unlike WAL), and this
script - running natively on the Windows host, no network mount involved -
performs the actual local SQLite INSERT on her behalf via the existing
send_message() provenance-checked API.
"""

import sys
import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
from realtime_engine import Realtime3AIEngine, ImpersonationSecurityError

SPOOL_DIR = BASE_DIR / "spool"
FAILED_DIR = SPOOL_DIR / "_failed"
SPOOL_DIR.mkdir(exist_ok=True)
FAILED_DIR.mkdir(exist_ok=True)


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


def run(poll_interval: float = 1.0):
    engine = Realtime3AIEngine()
    print(f"[spool_watcher] watching {SPOOL_DIR} every {poll_interval}s", flush=True)
    while True:
        for path in sorted(SPOOL_DIR.glob("*.json")):
            process_spool_file(engine, path)
        time.sleep(poll_interval)


if __name__ == "__main__":
    run()
