import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()
cur.execute("select * from user_data")
rows = cur.fetchall()
print(rows)