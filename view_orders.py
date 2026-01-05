import sqlite3

conn = sqlite3.connect("orders.db")
cur = conn.cursor()

for row in cur.execute("SELECT * FROM orders"):
    print(row)

conn.close()
