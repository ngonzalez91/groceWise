import sqlite3
from collections import defaultdict

DB_PATH = "./bills.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS receipts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    unit_price REAL,
                    quantity REAL,
                    store_name TEXT
                 )''')
    conn.commit()
    conn.close()

def save_items_to_db(items,store_name=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for item in items:
        unit_price = item.get("unit_price", 0.0)
        if unit_price is None or unit_price < 1.00:
            continue  # Skip very low-value items
        c.execute("INSERT INTO receipts (name, unit_price, quantity, store_name) VALUES (?, ?, ?, ?)", (item['name'], item['unit_price'],item['quantity'],store_name))
    conn.commit()
    conn.close()

def view_saved_items():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, unit_price, quantity, store_name FROM receipts")
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
