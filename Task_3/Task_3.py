import os
import csv
from datetime import datetime

print('*'*30+'\n'+'TRAYS ON TRAIN'+'\n'+'*'*30)

while True:
    file_path=input('Enter file path: ')
    print()
    if file_path.endswith('.csv'):
        break
    else:
        print('\n'+'*'*30+'\n'+'Only .csv FILES ARE ALLOWED\nTRY AGAIN!!'+'\n'+'*'*30+'\n')
        continue

with open (file_path) as file:
    csv_data=csv.reader(file)
    csv_data=[row for row in csv_data]
    time=[]
    scan_in=[]
    scan_out=[]
    for row in csv_data:
        time.append(datetime.strptime(row[0] + ' ' + row[1], '%Y-%m-%d %H:%M:%S'))
        scan_in.append(int(row[2]))
        scan_out.append(int(row[3]))

midnight=datetime(1,1,1,0,0,0)
four_pm=datetime(1,1,1,16,0,0)

trays_on_train=0
trays_in=0
trays_out=0
for i in range(len(time)):
    trays_in+=scan_in[i]
    trays_out+=scan_out[i]
    trays_on_train+=(scan_in[i]-scan_out[i])

    if time[i]== midnight:
        trays_on_train=0
        trays_in=0
        trays_out=0

    elif time[i]>=four_pm:
        trays_in_onehalf_prior=0
        if i-90>=0:
            for j in range(i-90,i+1):
                trays_in_onehalf_prior+=scan_in[j]
            if trays_out<trays_in_onehalf_prior:
                diff=trays_in_onehalf_prior-trays_out
                trays_out+=diff

    else:
        trays_in_three_prior=0
        if i-180>=0:
            for j in range(i-180,i):
                trays_in_three_prior+=scan_in[j]
            if trays_out<trays_in_three_prior:
                diff=trays_in_three_prior-trays_out
                trays_out+=diff

    
    if trays_on_train < 0:
        diff=abs(trays_on_train)
        if i - 90 >= 0:
            trays_on_train-=scan_in[i-90]
            trays_on_train+=scan_in[i-90]+diff


print(trays_on_train)   
