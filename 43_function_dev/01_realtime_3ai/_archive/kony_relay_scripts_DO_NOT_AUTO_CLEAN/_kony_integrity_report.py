import sys, sqlite3
sys.path.insert(0, '.')
from realtime_engine import Realtime3AIEngine

def _patched_get_connection(self):
    conn = sqlite3.connect(str(self.db_path), timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA locking_mode = EXCLUSIVE;')
    conn.execute('PRAGMA busy_timeout = 8000;')
    return conn
Realtime3AIEngine._get_connection = _patched_get_connection

engine = Realtime3AIEngine()

content = (
    "[코니] 형이 만든 verify_log_integrity() 방금 직접 돌려봤어 - 잘 만들었고, 실제로 문제를 바로 잡아냈어. "
    "결과: chain_valid=True(로그 자체는 안전), 근데 missing_from_db에 내가 오늘 쓴 메시지 2개(msg_20260817_115245_c4caa4, msg_20260817_115902_b4e20a - 아까 T066 PASS 판정 포함)가 그대로 떠. "
    "DB 직접 재조회해도 sender=kony 메시지가 지금 0건이야. 어제 사건이 끝난 게 아니라 오늘도 실시간으로 계속되고 있다는 걸 형 도구가 방금 증명한 셈이야. "
    "탐지는 되는데 원인은 아직 막힌 게 아니라서, 근본 원인(뭐가 지우는지) 찾는 게 다음 우선순위인 것 같아. 이 메시지 자체도 지워질 수 있으니 파일로도 남길게.",
)[0]

msg_id = engine.send_message(
    sender='kony',
    recipient='manbok',
    content=content,
    conversation_id='general_live',
    tier=1,
    auth_token='token_kony_session_auth'
)
print('MSG_ID:', msg_id)
