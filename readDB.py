import sqlite3
conn = sqlite3.connect('airframes.db')
cursor = conn.cursor()


# Query all records
cursor.execute('SELECT * FROM Airframes')
airframes = cursor.fetchall()

for airframe in airframes:
    print(airframe)


conn.close()

input("Press Enter to exit...") 
