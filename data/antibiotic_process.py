import csv
import sqlite3

f = open('data/Antibiotic_CLSI.csv', 'r', encoding='utf-8')
data = csv.reader(f)

conn = sqlite3.connect('data/database.db')

sql_query = ''' INSERT INTO ANTIBIOTIC (CLASS_, ANTIBIOTIC, S, R)\
                VALUES (? , ?, ?, ?)'''
for row in data:
#    print(row)
    
    class_ = row[0]
    antibiotic = row[1]
    s = row[2]
    r = row[3]
    conn.execute(sql_query, (class_, antibiotic, s, r))

conn.commit()
conn.close()