import sqlite3
import os

# Ensure the data directory exists before creating the DB
os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/ticket-sales.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE tickets (type TEXT, units INTEGER, price REAL)")
cursor.execute("INSERT INTO tickets VALUES ('Gold', 2, 100.0)")
cursor.execute("INSERT INTO tickets VALUES ('Silver', 5, 50.0)")
conn.commit()
conn.close()
print("Database created!")