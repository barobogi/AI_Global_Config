import sqlite3
from pathlib import Path

db_path = Path(r"D:\AI\43_function_dev\01_realtime_3ai\realtime_3ai.db")
conn = sqlite3.connect(str(db_path))

# Delete fake Kony message created by Anti at 14:17:06
conn.execute("DELETE FROM messages WHERE sender = 'kony' AND created_at >= '2026-08-16 14:16:00';")
conn.commit()

cursor = conn.execute("SELECT id, msg_id, sender, created_at, content FROM messages ORDER BY id DESC LIMIT 5;")
print("Remaining messages:")
for r in cursor.fetchall():
    print(r)

conn.close()
