import json
import csv
import time
import datetime

names =['Niklas Henschel', 'Janne Savikko', 'Leena Romppainen', 'Jussi Vaihia', 'Julia Shamrina', 'Jaakko Malkamäki', 'Tuomas Hietala', 'Laura Kiviluoma', 'Admin-janne Savikko']

def getdate(str):
    timeArray = time.strptime(str, "%Y-%m-%dT%H:%M:%S.000Z")
    year = int(time.strftime("%Y", timeArray))
    month = int(time.strftime("%m", timeArray))
    day = int(time.strftime("%d", timeArray))
    create_date = datetime.date(year, month, day)
    return create_date

days = 74
axis_start = datetime.date(2020,1,1)
axis_end = datetime.date(2020,3,14)

count = []
for i in range(4):
    row_arr = ["open"]
    for j in range(days):
        row_arr.append(0)
    count.append(row_arr)

for i in range(4):
    row_arr = ["solved"]
    for j in range(days):
        row_arr.append(0)
    count.append(row_arr)

for i in range(3):
    row_arr = ["all_status_num"]
    for j in range(days):
        row_arr.append(0)
    count.append(row_arr)

for i in range(0, days):
    if (i > -1):
        print(i)
        current_date = axis_start + datetime.timedelta(days=i)
        with open('raw.json', 'r', encoding='UTF-8') as rf:
            for row in rf:
                ticket = json.loads(row)
                if (ticket['assignee'] and ticket['assignee']['name'] in names):
                    create_date = getdate(ticket['created_at'])
                    if (ticket['status'] == 'open'):  
                        open_delta = current_date.__sub__(create_date).days
                        if (open_delta > 0 and open_delta < 30):
                            count[0][i+1] = count[0][i+1] + 1
                        if (open_delta >= 30 and open_delta < 60):
                            count[1][i+1] = count[1][i+1] + 1
                        if (open_delta >= 60 and open_delta < 90):
                            count[2][i+1] = count[2][i+1] + 1
                        if (open_delta >= 90):
                            count[3][i+1] = count[3][i+1] + 1
                    elif (ticket['status'] == 'solved'):
                        solved_date = getdate(ticket['dates']['solved_at'])
                        if (current_date >= solved_date):
                            solved_delta = solved_date.__sub__(create_date).days
                            if (solved_delta > 0 and solved_delta < 30):
                                count[4][i+1] = count[4][i+1] + 1
                            if (solved_delta >= 30 and solved_delta < 60):
                                count[5][i+1] = count[5][i+1] + 1
                            if (solved_delta >= 60 and solved_delta < 90):
                                count[6][i+1] = count[6][i+1] + 1
                            if (solved_delta >= 90):
                                count[7][i+1] = count[7][i+1] + 1

                    if (current_date.__sub__(create_date).days > 0):
                        if (ticket['status'] == 'open'):
                            count[8][i+1] = count[8][i+1] + 1
                            #print(create_date,current_date)
                        elif (ticket['status'] == 'closed'):
                            count[9][i+1] = count[9][i+1] + 1
                            #print(create_date, current_date)
                      
                            #print(create_date, current_date)
            rf.close()
            print(count[0][i + 1], count[1][i + 1], count[2][i + 1], count[3][i + 1])
            print(count[4][i + 1], count[5][i + 1], count[6][i + 1], count[7][i + 1])
            print(count[8][i+1], count[9][i+1], count[10][i+1])


with open('open.csv', 'w', encoding='UTF-8') as wf:
    writer = csv.writer(wf, delimiter=',', lineterminator='\n')
    head = ["status"]
    for i in range(days):
        head.append(i)
    writer.writerow(head)
    for row in count:
        writer.writerow(row)


'''with open('raw.json', 'r', encoding='UTF-8') as rf:
    for i,row in enumerate(rf):
        ticket = json.loads(row)
        if (ticket['status'] == 'solved'):
            print(ticket['dates']['solved_at'],i)
    rf.close()'''