import sqlite3

DB_PATH = "bills.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS receipts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    unit_price REAL,
                    quantity REAL
                 )''')
    conn.commit()
    conn.close()

def save_items_to_db(items):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for item in items:
        c.execute("INSERT INTO receipts (name, unit_price, quantity) VALUES (?, ?, ?)", (item['name'], item['unit_price'],item['quantity']))
    conn.commit()
    conn.close()

def view_saved_items():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, unit_price, quantity FROM receipts")
    rows = c.fetchall()
    conn.close()
    return rows
