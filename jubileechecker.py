import csv
import sys

from datetime import date, datetime

file = sys.argv[1]
reference_year = int(sys.argv[2])

def is_birthday_like(row):
    return (row != []) and (row[0] in ['b', 'a'])

with open(file) as csvfile:
    reader = csv.reader(csvfile, skipinitialspace=True)
    for row in reader:
        if is_birthday_like(row):
            year = datetime.strptime(row[1], '%Y-%m-%d').year
            age = reference_year - year
            if (age % 5 == 0):
                print(f'{row[0]}-{row[2]}: {age} years')