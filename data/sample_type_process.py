import csv
from textwrap import indent
import json

f = open('data/sample_type.txt', encoding = 'utf-8', errors = 'ignore')
sample_type = {}
for row in f:
    data = row.split('\t')
    print(data)
    sample_type[str(data[0])] = data[2].strip('\n')
f.close()

f = open('data/SAMPLE_TYPE.json','w', encoding = 'utf-8')
json.dump(sample_type, f, indent = 4) 
f.close()

f = open('data/SAMPLE_TYPE.json','r', encoding = 'utf-8')
data = json.load(f)
f.close()
for row in data:
    print(row)