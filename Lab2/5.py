import pandas as pd
import os
import json

data = pd.read_csv("DARWIN.csv", delimiter=',')
#print(data)

# Выбор полей
selected_fields = data[['air_time1', 'ID', 'paper_time1', 'air_time2', 'gmrt_in_air1', 'num_of_pendown2', 'class']]

# Расчет характеристик для числовых полей
numerical = ['air_time1', 'paper_time1', 'air_time2', 'gmrt_in_air1', 'num_of_pendown2']
stats = {}

for field in numerical:
    stats[field] = {
        # преобразование в int или float для работы с json
        'min': int(data[field].min()),
        'max': int(data[field].max()),
        'mean': float(data[field].mean()),
        'sum': float(data[field].sum()),
        'std': float(data[field].std())
    }

# Расчет частоты встречаемости для P (Пациентов) и H (Здоровых людей)
text_field = 'class'
frequency = data[text_field].value_counts(normalize=True).to_dict()

# Сохранение расчетов в json
with open('stats.json', 'w') as json_file:
    json.dump(stats, json_file)

with open('frequency.json', 'w') as json_file:
    json.dump(frequency, json_file)

# Сохранение набора данных в разных форматах
data.to_csv('data.csv', index=False)
data.to_json('data.json', orient='records')

data.to_pickle('data.pkl')

print('Size of stats.json:', os.path.getsize('stats.json'))
print('Size of frequency.json:', os.path.getsize('frequency.json'))
print('Size of data.csv:', os.path.getsize('data.csv'))
print('Size of data.json:', os.path.getsize('data.json'))
print('Size of data.pkl:', os.path.getsize('data.pkl'))

#Возможно файл меньше нужного размера, но у меня почему-то не импортировался файл бОльшего размера и читался не полностью, выдавая ошибки