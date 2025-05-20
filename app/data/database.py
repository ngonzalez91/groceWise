import sqlite3
import os
import json
from collections import defaultdict
from datetime import datetime
from app.core.ocr import extract_text
from app.services.ai_parser import parse_structured_receipt

DB_PATH = "./bills.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS receipts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    category_name TEXT,
                    unit_price REAL,
                    quantity REAL,
                    store_name TEXT
                 )''')
    c.execute("""
        CREATE TABLE IF NOT EXISTS incomplete_receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            store_name TEXT,
            receipt_json TEXT
        )
    """)
    conn.commit()
    conn.close()

def process_receipt(path):
    abs_path = os.path.abspath(path)
    print("[INFO] Extracting text from:", abs_path)
    raw_text = extract_text(abs_path)

    print("[INFO] Parsing structured receipt using AI...")
    structured = parse_structured_receipt(raw_text)

    if 'items' in structured:
        store = structured.get("store", {})
        store_name = store.get("name", "Unknown")
        print("[INFO] Saving items to database...")
        items = structured.get("items", [])
    has_nulls = any(
        i.get("name") is None or
        i.get("category_name") is None or
        i.get("quantity") is None or
        i.get("unit_price") is None or
        i.get("total_price") is None
        for i in items
    )
    if has_nulls:
        save_incomplete_receipt(structured)
    else:
        save_items_to_db(items, store_name=store_name)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"receipt_{ts}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, ensure_ascii=False, indent=2)

    return structured, out_path

def save_items_to_db(items,store_name=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for item in items:
        unit_price = item.get("unit_price", 0.0)
        if unit_price is None or unit_price < 1.00:
            continue  # Skip very low-value items
        c.execute("INSERT INTO receipts (name, category_name, unit_price, quantity, store_name) VALUES (?, ?, ?, ?, ?)", (item['name'], item['category_name'], item['unit_price'],item['quantity'],store_name))
    conn.commit()
    conn.close()

from datetime import datetime

def save_incomplete_receipt(structured):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    store_name = structured.get("store", {}).get("name", "Unknown")
    timestamp = datetime.now().isoformat()
    c.execute("""
        INSERT INTO incomplete_receipts (timestamp, store_name, receipt_json)
        VALUES (?, ?, ?)
    """, (timestamp, store_name, json.dumps(structured)))
    conn.commit()
    conn.close()
    print("[!] Incomplete receipt saved for later review.")


def view_saved_items():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, category_name, unit_price, quantity, store_name FROM receipts")
    rows = c.fetchall()
    conn.close()
    return rows

def compare_prices():
    conn = sqlite3.connect("./bills.db")
    c = conn.cursor()
    c.execute("""
        SELECT n.canonical_name, r.store_name, r.unit_price
        FROM receipts r
        JOIN item_normalization n ON r.name = n.variant_name
        ORDER BY n.canonical_name, r.store_name
    """)
    rows = c.fetchall()
    conn.close()

    grouped = defaultdict(lambda: defaultdict(list))
    for canonical, store, price in rows:
        grouped[canonical][store].append(price)

    print("\n--- Price Comparison by Store ---")
    for canonical, store_data in grouped.items():
        print(f"\n🛒 {canonical}")
        for store, prices in store_data.items():
            prices_str = ", ".join(f"${p:.2f}" for p in prices)
            print(f"  {store:20} → {prices_str}")

def process_all_receipts_in_folder(folder_path):
    print(f"[INFO] Scanning folder: {folder_path}")
    valid_exts = (".pdf", ".jpg", ".jpeg", ".png")

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_exts)]
    files.sort()

    if not files:
        print("[INFO] No receipts found.")
        return

    for file in files:
        full_path = os.path.join(folder_path, file)
        print(f"\n[PROCESSING] {file}")
        try:
            result, json_path = process_receipt(full_path)
            print(f"[✔] Saved to {json_path}")
        except Exception as e:
            print(f"[ERROR] Failed to process {file}: {e}")
