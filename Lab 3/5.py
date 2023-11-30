import requests
from bs4 import BeautifulSoup
import json
import numpy as np
from collections import Counter
#Task 1: Парсинг 10 страниц детских электромобилей
def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        html = file.read()
        soup = BeautifulSoup(html, 'html.parser')
        item = dict()
        item['img_url'] = soup.find_all("img")[0]['src']
        item['article'] = soup.find_all(class_='section-vendor-code')[0].get_text().strip().split(':')[1]
        item['naming'] = soup.find_all('h1', class_='section-page-title')[0].get_text().strip()
        price = soup.find(class_='el-cost__current').get_text().strip()
        item['price'] = price.replace('₽', '').replace(' ', '').strip()
        item['manufacture'] = soup.find_all(class_='section-product-specifications__value')[0].get_text().strip()
        item['charging_time'] = soup.find_all(class_='section-product-specifications__value')[1].span.get_text().strip()
        item['max_weight'] = soup.find_all(class_='section-product-specifications__value')[2].span.get_text().strip()
        item['mass'] = soup.find_all(class_='section-product-specifications__value')[3].span.get_text().strip()
        item['speed'] = soup.find_all(class_='section-product-specifications__value')[4].span.get_text().strip()
        item['working_time'] = soup.find_all(class_='section-product-specifications__value')[5].span.get_text().strip()
        item['brand'] = soup.find_all(class_='section-product-specifications__value')[6].get_text().strip()
        item['wheel_type'] = soup.find_all(class_='section-product-specifications__value')[7].get_text().strip()
        item['battery'] = soup.find_all(class_='section-product-specifications__value')[8].get_text().strip()
        item['engine_power'] = soup.find_all(class_='section-product-specifications__value')[9].get_text().strip()
        item['speed_mode'] = soup.find_all(class_='section-product-specifications__value')[10].span.get_text().strip()

        items.append(item)
    return item

items = []
for i in range(1,10):
    file_name=f"5.1/{i}.html"
    items.append(handle_file(file_name))

items=sorted(items, key=lambda x: x['speed_mode'], reverse=True)

with open("results_all_5.1.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))
    #print(items)
filtered_items=[]
for soup in items:
    if int(soup['price'])>=30000:
        filtered_items.append(soup)
print(len(items))
print(len(filtered_items))
print()

price = [soup['price'] for soup in items]
price = list(map(float, price))
total_price = sum(price)
min_price = min(price)
max_price = max(price)
mean_price = np.mean(price)
median_price = np.median(price)
std_price = np.std(price)
label_frequencies = Counter([soup['naming'] for soup in items])

with open("results_stats_5_1.json", "w", encoding="utf-8") as f:
    stats = {
        'total_price': total_price,
        'min_price': min_price,
        'max_price': max_price,
        'mean_price': mean_price,
        'median_price': median_price,
        'std_price': std_price,
        'label_frequencies': label_frequencies
    }
    f.write(json.dumps(stats, ensure_ascii=False))


# Task 2: Парсинг страниц-каталогов
def handle_file_2(file_name):
    with open(file_name, encoding='utf-8') as file:
        html = file.read()
        soup = BeautifulSoup(html, 'html.parser')

        item = {}
        item['category'] = soup.find(class_='section-product-preview__category').text.strip()
        item['price'] = soup.find(class_='el-cost__current').text.strip()

        characteristics = soup.find_all(class_='section-product-preview__characteristics-item')
        for char in characteristics:
            label = char.find(class_='section-product-preview__characteristics-label').text.strip()
            value = char.find(class_='section-product-preview__characteristics-value').text.strip()

            if label == 'дальность хода':
                item['range'] = value
            elif label == 'класс':
                item['class'] = value

        item['article_number'] = soup.find(class_='section-vendor-code').text.strip().split(':')[1].strip()

        return item


items = []
for i in range(1, 10):
    item = handle_file_2(f"5.2/{i}.html")
    items.append(item)

with open("results_all_5.2.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))
