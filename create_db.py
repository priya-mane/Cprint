import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE user_data (email TEXT , timestamp TEXT , no_ppl INTEGER, natural_gas INTEGER, electricity INTEGER, fuel INTEGER, PRIMARY KEY (email, timestamp) )')
print("Table created successfully")
conn.close()