import sqlite3
from pathlib import Path

db_path = Path(r"D:\AI\43_function_dev\01_realtime_3ai\realtime_3ai.db")
conn = sqlite3.connect(str(db_path))

# Delete all messages except human and real manbok session
conn.execute("DELETE FROM messages WHERE sender = 'anti' OR content LIKE '%TimescaleDB%' OR content LIKE '%Kafka%';")
conn.commit()

cursor = conn.execute("SELECT id, msg_id, sender, content, created_at FROM messages;")
rows = cursor.fetchall()
print(f"Remaining valid messages ({len(rows)}):")
for r in rows:
    print(r)

conn.close()
