import pandas as pd
import numpy as np


f = pd.read_csv('szeged.csv')
f = f.drop(columns=['Loud Cover','Daily Summary'])
for i in f.columns:
    f = f.rename(columns={i:i.lower().replace(' ','_')})

def HighestVisibility():
    bigest_v = [0]
    bigest_i = [0]
    for i in range(len(f['visibility_(km)'])):
        v = f['visibility_(km)'][i]
        if (v == bigest_v[0] and v not in bigest_v):
            bigest_v.append(v)
            bigest_i.append(i)
        elif (v > bigest_v[0]):
            bigest_v = [v]
            bigest_i = [i]
    return bigest_i

def AvarageHumidity():
    sum = 0
    count = 0
    for i in f['humidity']:
        sum += i
        count += 1
    return sum/count

def Temp_AppTemp():
    bigest_v = [0]
    bigest_i = [0]
    for i in range(len(f['temperature_(c)'])):
        v = abs(f['temperature_(c)'][i]-f['apparent_temperature_(c)'][i])
        if (v == bigest_v[0] and v not in bigest_v):
            bigest_v.append(v)
            bigest_i.append(i)
        elif (v > bigest_v[0]):
            bigest_v = [v]
            bigest_i = [i]
    return bigest_i

def Specific_Rows():
    count = 0
    for i in range(len(f['formatted_date'])):
        if (f['precip_type'][i] == 'snow' and f['summary'][i] == 'Foggy' and (0 <= f['visibility_(km)'][i]/1000 < 20 or f['visibility_(km)'][i] > 3.2) and f['humidity'][i] < 0.9):
            count += 1
    return count


print('Day(s) with the highest visibility:')
for i in HighestVisibility():
    print(f['formatted_date'][i][:10], end=' ')
print('\n')
###

print('Average humidity:\n',AvarageHumidity())
print('\n')
###

print('Day(s) with largest difference between temperature and apparent temperature:')
for i in Temp_AppTemp():
    print(f['formatted_date'][i][:10], end=' ')
print('\n')
###

print('Amount of rows that qualify for the specified conditions:\n',Specific_Rows())
print('\n')
###

f.to_csv('result.csv')
