import sqlite3

con = sqlite3.connect("database.db")

cur = con.cursor()
data = [
    ("abc@gmail.com","2021-08-31",4,7495, 600, 164),
    ("abc@gmail.com","2021-09-30",4,8345, 546, 120),
    ("abc@gmail.com","2021-10-31",4,7564, 700, 179),
    ("abc@gmail.com","2021-11-30",4,9675, 900, 100),
    ("abc@gmail.com","2021-12-31",4,9888, 678, 187),

    ("xyz@gmail.com","2021-08-31",2,3678, 300, 89),
    ("xyz@gmail.com","2021-09-30",2,3546, 298, 94),
    ("xyz@gmail.com","2021-10-31",2,2890, 340, 100),
    ("xyz@gmail.com","2021-11-30",2,3006, 200, 86),
    ("xyz@gmail.com","2021-12-31",2,2905, 278, 88),

    ("qrs@gmail.com","2021-08-31",1,1839, 150, 50),
    ("qrs@gmail.com","2021-09-30",1,1788, 149, 55),
    ("qrs@gmail.com","2021-10-31",1,1900, 155, 57),
    ("qrs@gmail.com","2021-11-30",1,1600, 167, 52),
    ("qrs@gmail.com","2021-12-31",1,1768, 147, 57),

    ("def@gmail.com","2021-08-31",2,2903, 320, 90),
    ("def@gmail.com","2021-09-30",2,3008, 330, 95),
    ("def@gmail.com","2021-10-31",2,2945, 298, 84),
    ("def@gmail.com","2021-11-30",2,2893, 378, 88),
    ("def@gmail.com","2021-12-31",2,3840, 377, 94),

    ("ijk@gmail.com","2021-08-31",1,1078, 156, 45),
    ("ijk@gmail.com","2021-09-30",1,1508, 99, 55),
    ("ijk@gmail.com","2021-10-31",1,978, 104, 56),
    ("ijk@gmail.com","2021-11-30",1,1208, 90, 67),
    ("ijk@gmail.com","2021-12-31",1,1099, 120, 56),

]

for d in data:
    cur.execute("INSERT INTO user_data (email, timestamp, no_ppl, natural_gas, electricity, fuel) VALUES (?,?,?,?,?,?)", d )
    con.commit()

con.close()