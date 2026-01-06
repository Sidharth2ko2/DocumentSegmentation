import sqlite3


conn = sqlite3.connect("storage.db", check_same_thread=False)
cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS documents (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
text TEXT,
label TEXT,
confidence REAL
)
""")


conn.commit()