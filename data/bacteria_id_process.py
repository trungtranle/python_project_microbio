import csv
import sqlite3

f = open('data/bacteria_id.csv', 'r', encoding='utf-8')
data = csv.reader(f)

conn = sqlite3.connect('data/database.db')

sql_query = ''' INSERT INTO BACTERIA_ID (NAME, CLASS_)\
                VALUES (? , ?)'''
for row in data:
#    print(row)
    name = row[1]
    class_ = row[2]
    conn.execute(sql_query, (name, class_,))

conn.commit()
conn.close()