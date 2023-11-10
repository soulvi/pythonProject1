from bs4 import BeautifulSoup
import re
import json
import numpy as np
from collections import Counter

def handle_file(file_name):
    items=list()
    with open(file_name, encoding='utf-8') as file:
        text = ""
        for row in file.readlines():
            text += row

        root = BeautifulSoup(text, 'xml')
        for clothing in root.find_all("clothing"):
            item=dict()
            for el in clothing.contents:
                if el.name is None:
                    continue
                elif el.name=="price" or el.name=="reviews":
                    item[el.name]=int(el.get_text().strip())
                elif el.name=="price" or el.name=="rating":
                    item[el.name]=float(el.get_text().strip())
                elif el.name=="new":
                    item[el.name]=el.get_text().strip()=="+"
                elif el.name=="exclusive" or el.name=="sporty":
                    item[el.name]=el.get_text().strip()=="yes"
                else:
                    item[el.name]=el.get_text().strip()
            items.append(item)
    return items


items=[]
for i in range(1,100):
    file_name=f"4/{i}.xml"
    items+=handle_file(file_name)

items=sorted(items, key=lambda x: x['price'], reverse=True)

with open("results_all_4.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items))

filtered_items=[]
for root in items:
    if root['reviews']>=500000:
        filtered_items.append(root)

print(len(items))
print(len(filtered_items))
print()

price = [clothing['price'] for clothing in items]
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
titles = [clothing['name'] for clothing in filtered_items]
label_frequencies = Counter(titles)

for label, frequency in label_frequencies.items():
    print(f'{label}: {frequency}')