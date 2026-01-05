import sqlite3

conn = sqlite3.connect("orders.db")
cur = conn.cursor()

for row in cur.execute("SELECT * FROM products"):
    print(row)

conn.close()
