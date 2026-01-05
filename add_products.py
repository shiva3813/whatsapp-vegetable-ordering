import sqlite3

products = [
    ("Apple", 60, "apple.jpg"),
    ("Banana", 50, "banana.jpg"),
    ("Watermelon", 40, "watermelon.jpg"),
    ("Spinach", 30, "spinach.jpg"),
    ("Onion", 40, "onion.jpg"),
    ("Tomato", 30, "tomato.jpg")
]

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

cur.execute("DELETE FROM products")

for p in products:
    cur.execute(
        "INSERT INTO products (name, price, image) VALUES (?,?,?)",
        p
    )

conn.commit()
conn.close()

print("✅ Products added successfully")
