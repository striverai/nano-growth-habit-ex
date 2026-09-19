import sqlite3
import datetime
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

src = 'brain.db'
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
backup_filename = f'brain_backup_{timestamp}.db'

# Use SQLite online backup API for 100% transactionally safe backup
conn_src = sqlite3.connect(src)
conn_dst = sqlite3.connect(backup_filename)
with conn_dst:
    conn_src.backup(conn_dst)
conn_dst.close()
conn_src.close()

# Verify integrity of backup
check_conn = sqlite3.connect(backup_filename)
c = check_conn.cursor()
c.execute("PRAGMA integrity_check")
integrity = c.fetchone()[0]
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]
check_conn.close()

size = os.path.getsize(backup_filename)
print(f"BACKUP_SUCCESS: {backup_filename}")
print(f"FILE_SIZE: {size:,} bytes")
print(f"INTEGRITY_CHECK: {integrity}")
print(f"BACKED_UP_TABLES: {', '.join(tables)}")
