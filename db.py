import sqlite3

def init_db():
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        image TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT,
        product TEXT,
        quantity INTEGER,
        status TEXT,
        image TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_order(phone, product, quantity):
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()

    cur.execute("SELECT image FROM products WHERE name=?", (product,))
    img = cur.fetchone()
    image = img[0] if img else ""

    cur.execute(
        "INSERT INTO orders (phone, product, quantity, status, image) VALUES (?,?,?,?,?)",
        (phone, product, quantity, "CONFIRMED", image)
    )

    conn.commit()
    conn.close()


def get_products():
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_orders():
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_order_counts():
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM orders")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders WHERE status='CONFIRMED'")
    confirmed = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders WHERE status='DELIVERED'")
    delivered = cur.fetchone()[0]

    conn.close()
    return total, confirmed, delivered

def update_status(order_id):
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status='DELIVERED' WHERE id=?", (order_id,))
    conn.commit()
    conn.close()


