import csv
aver_salary=0
items=list()
with open('text_4', newline='\n', encoding='utf-8') as file:
    reader =csv.reader(file, delimiter=',')
    for row in reader:
        print(row)

        item={
            'number': int(row[0]),
            'name': row[2]+' '+row[1],
            'age':int(row[3]),
            'salary':int(row[4][0:-1])
        }
        aver_salary += item['salary']
        items.append(item)
'[0:-1]-срез чтобы обрезать знак Рубля'


print(items)
aver_salary/=len(items)
'Для среднего'

filtered=list()
for item in items:
    if (item['salary']>aver_salary) and item['age']>25+58 % 10:
        filtered.append(item)
filtered=sorted(filtered, key=lambda i: i['number'])

with open('r_text_4.txt', 'w', encoding="utf-8", newline='') as result:
    writer = csv.writer(result,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for item in filtered:
        writer.writerow(item.values())
