import os
import csv
from main import question_num

dot = (os.path.dirname(__file__)).replace('\\','/')

last_val = 0

file_path = f'{dot}/Data/threshes.csv'

rows = [
    '',
    'medium',
    'hard',
    'start',
    'l',
    '.',
] + [f'q{i}' for i in range(1,question_num+1)] + ['.'] + [f'a{i}' for i in range(1,question_num+1)] + [
    '.',
    'p8',
    'p4',
    'm4',
    'p14',
    'p6',
    'new',
    '...'
]

data = [ {'img':imgname}  for imgname in rows]

with open(file_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['img','thresh'])
    writer.writeheader()
    writer.writerows(data)
