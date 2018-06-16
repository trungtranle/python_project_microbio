import math
import tkinter
from tkinter.constants import VERTICAL, ALL
from tkinter import N, E, W, S, NS
import sqlite3

conn = sqlite3.connect('data/database.db')
query = '''SELECT ANTIBIOGRAM FROM SAMPLE_INFO WHERE SID = 654321 '''
data = conn.execute(query)
for row in data:
    print(row)
    '''print(row[0])
    dic = eval(row[0])
    print(dic)
    print(dic.keys())
    print(dic['AMC'][1])
    for key in '''
