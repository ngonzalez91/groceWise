import sqlite3

DB_PATH = "bills.db"

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
