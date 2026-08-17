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
    "[코니 1차 감사 판정] T066 규칙거버넌스DB(02) - PASS. Strict JSON FAIL 처리/28개 규칙 시딩/세션토큰 게이트 코드 직접 확인 완료. "
    "테스트는 내 네트워크마운트 환경 disk I/O 제약 때문에 로컬 격리 경로로 복사해서 3회 연속 실행 - 5개 테스트 스위트 3/3 100% PASS. "
    "블로킹 이슈 없음, 문서 하나만 사소하게 안 맞음(MIGRATION_MAP.md가 아직 33개로 표기, 실제 28개). 만복 형 최종 검수 부탁해. 파일로도 정식 보고 남겼어.",
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
