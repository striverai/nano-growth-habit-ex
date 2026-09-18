"""
setup_tables.py
Tạo 3 bảng mới trong brain.db:
  - products   : sản phẩm (physical/digital/service)
  - customers  : khách hàng (import từ waitlist.json nếu có)
  - orders     : đơn hàng (liên kết customers <-> products)
"""

import sqlite3
import json
import os
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH  = "brain.db"
WAITLIST = "waitlist.json"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
cur  = conn.cursor()

# ─────────────────────────────────────────
# 1. TẠO BẢNG products
# ─────────────────────────────────────────
cur.executescript("""
CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    type        TEXT    NOT NULL CHECK(type IN ('physical','digital','service')),
    price       INTEGER NOT NULL,
    description TEXT,
    stock       INTEGER,
    is_active   INTEGER NOT NULL DEFAULT 1,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
print("OK Bang products da tao.")

# ─────────────────────────────────────────
# 2. TẠO BẢNG customers
# ─────────────────────────────────────────
cur.executescript("""
CREATE TABLE IF NOT EXISTS customers (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    phone         TEXT    NOT NULL UNIQUE,
    zalo          TEXT,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    note          TEXT
);
""")
print("OK Bang customers da tao.")

# ─────────────────────────────────────────
# 3. TẠO BẢNG orders
# ─────────────────────────────────────────
cur.executescript("""
CREATE TABLE IF NOT EXISTS orders (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id  INTEGER NOT NULL REFERENCES customers(id),
    product_id   INTEGER NOT NULL REFERENCES products(id),
    quantity     INTEGER NOT NULL DEFAULT 1,
    amount       INTEGER NOT NULL,
    status       TEXT    NOT NULL DEFAULT 'pending'
                         CHECK(status IN ('pending','success','cancelled','refunded')),
    payment_code TEXT    UNIQUE,
    note         TEXT,
    ordered_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paid_at      TIMESTAMP
);
""")
print("OK Bang orders da tao.")

conn.commit()

# ─────────────────────────────────────────
# 4. SEED products (3 goi Nano Growth Habit EX)
# ─────────────────────────────────────────
packages = [
    {
        "name": "Nano Growth Habit EX - Goi Trai Nghiem (1 hop)",
        "type": "physical",
        "price": 1250000,
        "description": "1 hop 120 vien, dung ~2 thang. Tang mien phi van chuyen.",
        "stock": None,
    },
    {
        "name": "Nano Growth Habit EX - Goi Chuan Dot Pha (2 hop)",
        "type": "physical",
        "price": 2350000,
        "description": "2 hop 240 vien, dung ~4 thang. Tang thuoc do decal + cam nang Nhat Ban + ship hoa toc.",
        "stock": None,
    },
    {
        "name": "Nano Growth Habit EX - Goi Toan Dien (3 hop)",
        "type": "physical",
        "price": 3390000,
        "description": "3 hop 360 vien (Mua 2 Tang 1), dung ~6 thang. Tang men vi sinh Nhat + thuoc do + ship + tu van 1-1.",
        "stock": None,
    },
]

added = 0
for p in packages:
    cur.execute("SELECT id FROM products WHERE name = ?", (p["name"],))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO products (name, type, price, description, stock) VALUES (?,?,?,?,?)",
            (p["name"], p["type"], p["price"], p["description"], p["stock"])
        )
        added += 1

conn.commit()
print(f"OK products: them {added} san pham moi.")

# ─────────────────────────────────────────
# 5. IMPORT customers tu waitlist.json
# ─────────────────────────────────────────
if os.path.exists(WAITLIST):
    with open(WAITLIST, encoding="utf-8") as f:
        waitlist = json.load(f)

    imported = 0
    skipped  = 0
    errors   = 0

    if isinstance(waitlist, dict):
        waitlist = waitlist.get("data", waitlist.get("customers", []))

    for entry in waitlist:
        name  = (entry.get("name") or entry.get("ho_ten") or entry.get("full_name") or "").strip()
        phone = (entry.get("phone") or entry.get("so_dien_thoai") or entry.get("sdt") or "").strip()
        zalo  = (entry.get("zalo") or entry.get("zalo_number") or phone).strip()
        reg   = entry.get("registered_at") or entry.get("created_at") or datetime.now().isoformat()
        note  = entry.get("note") or entry.get("ghi_chu") or ""

        if not phone:
            errors += 1
            continue

        try:
            cur.execute(
                "INSERT OR IGNORE INTO customers (name, phone, zalo, registered_at, note) VALUES (?,?,?,?,?)",
                (name, phone, zalo, reg, note)
            )
            if cur.rowcount:
                imported += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  LOI import {phone}: {e}")
            errors += 1

    conn.commit()
    print(f"OK customers: import {imported} moi, bo qua trung {skipped}, loi {errors}.")
else:
    print(f"CANH BAO: Khong tim thay '{WAITLIST}'")
    print("  -> Bang customers de trong. Dat file waitlist.json vao thu muc va chay lai.")

conn.close()

# ─────────────────────────────────────────
# 6. XEM LAI KET QUA
# ─────────────────────────────────────────
print("\n" + "-"*55)
print("KET QUA:")
conn2 = sqlite3.connect(DB_PATH)
c2    = conn2.cursor()
for tbl in ["products", "customers", "orders"]:
    c2.execute(f"SELECT COUNT(*) FROM {tbl}")
    count = c2.fetchone()[0]
    c2.execute(f"PRAGMA table_info({tbl})")
    cols = [row[1] for row in c2.fetchall()]
    print(f"  {tbl:12s} | {count:3d} rows | {', '.join(cols)}")

print("\nSan pham hien co:")
c2.execute("SELECT id, name, price, type, stock FROM products ORDER BY price")
for row in c2.fetchall():
    stock_str = f"{row[4]} con" if row[4] is not None else "khong gioi han"
    print(f"  [{row[0]}] {row[1][:50]} | {row[2]:,}d | {row[3]} | {stock_str}")

conn2.close()
print("-"*55)
print("HOAN TAT! brain.db da cap nhat.")
