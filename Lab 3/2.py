from bs4 import BeautifulSoup
import re
import json
import numpy as np
from collections import Counter

def handle_file(file_name):
    items=list()
    with open(file_name, encoding='utf-8') as file:
        text= ""
        for row in file.readlines():
            text+=row

        site=BeautifulSoup(text, 'html.parser')
        products=site.find_all("div", attrs={'class':'product-item'})
        for product in products:
            item=dict()
            item['id']=product.a['data-id']
            item['link']=product.find_all('a')[1]['href']
            item['img_url']=product.find_all("img")[0]['src']
            item['title']=product.find_all("span")[0].get_text().strip()
            item['price']=int(product.price.get_text().replace("₽","").replace(" ", "").strip())
            item['bonus']=int(product.strong.get_text().replace("+ начислим ", "").replace("бонусов", "").strip())

            props=product.ul.find_all("li")
            for prop in props:
                item[prop['type']]=prop.get_text().strip()

            items.append(item)
        return items

items=[]
for i in range(1,32):
    file_name=f"2/{i}.html"
    items+=handle_file(file_name)

items=sorted(items, key=lambda x: x['price'], reverse=True)
with open("results_all_2.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items))

filtered_items=[]
for phone in items:
    if phone['bonus']>=3000:
        filtered_items.append(phone)

print(len(items))
print(len(filtered_items))
print()

price = [phone['price'] for phone in items]

total_price = np.sum(price)
min_price = np.min(price)
max_price = np.max(price)
mean_price = np.mean(price)
median_price = np.median(price)
std_price = np.std(price)

print('Price:')
print(f'Total: {total_price}')
print(f'Minimum: {min_price}')
print(f'Maximum: {max_price}')
print(f'Mean: {mean_price}')
print(f'Median: {median_price}')
print(f'Standard Deviation: {std_price}')
print()


# Частота
titles = [phone['title'] for phone in filtered_items]
label_frequencies = Counter(titles)

for label, frequency in label_frequencies.items():
    print(f'{label}: {frequency}')



