import sys, sqlite3, importlib
sys.path.insert(0, '.')
import test_rule_governance as trg
from rule_engine import RuleGovernanceEngine

def _patched_get_connection(self, readonly=False):
    conn = sqlite3.connect(str(self.db_path), timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA locking_mode = EXCLUSIVE;')
    conn.execute('PRAGMA busy_timeout = 8000;')
    if readonly:
        conn.execute('PRAGMA query_only = ON;')
    return conn
RuleGovernanceEngine._get_connection = _patched_get_connection

for i in range(1, 4):
    print(f"===== RUN {i} =====")
    try:
        trg.cleanup_test_files()
    except Exception as e:
        print("cleanup warn:", e)
    try:
        trg.run_all_tests()
    except Exception as e:
        print("RUN FAILED:", type(e).__name__, e)
