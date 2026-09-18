import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('brain.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()
print("Tables:", tables)
for t in tables:
    print(f"\n--- Table: {t[0]} ---")
    c.execute(f"PRAGMA table_info({t[0]})")
    cols = c.fetchall()
    for col in cols:
        print(f"  {col[1]} ({col[2]})")
    c.execute(f"SELECT COUNT(*) FROM {t[0]}")
    print(f"  Row count: {c.fetchone()[0]}")
conn.close()
