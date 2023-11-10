from bs4 import BeautifulSoup
import re
import json
import numpy as np
from collections import Counter

def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ""
        for row in file.readlines():
            text += row

        star=BeautifulSoup(text, 'xml').star
        item=dict()
        item['name']=star.find_all("name")[0].get_text().strip()
        item['constellation'] = star.find_all("constellation")[0].get_text().strip()
        item['spectral-class'] = star.find_all("spectral-class")[0].get_text().strip()
        item['radius'] = star.find_all("radius")[0].get_text().strip()
        item['rotation'] = star.find_all("rotation")[0].get_text().strip()
        item['age']=float(star.age.get_text().replace("billion years","").replace(" ", "").strip())
        item['distance'] = star.find_all("distance")[0].get_text().strip()
        item['absolute-magnitude'] = star.find_all("absolute-magnitude")[0].get_text().strip()
        return item

handle_file("3/58.xml")
items=[]
for i in range(1,500):
    file_name=f"3/{i}.xml"
    result=handle_file(file_name)
    items.append(result)

items=sorted(items, key=lambda x: x['radius'], reverse=True)

with open("results_all_3.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items))

filtered_items=[]
for star in items:
    if star['age']>=4.5:
        filtered_items.append(star)

print(len(items))
print(len(filtered_items))
print()

radius = [star['radius'] for star in items]
radius = list(map(float, radius))
total_radius = np.sum(radius)
min_radius = np.min(radius)
max_radius = np.max(radius)
mean_radius = np.mean(radius)
median_radius = np.median(radius)
std_radius = np.std(radius)

print('Views:')
print(f'Total: {total_radius}')
print(f'Minimum: {min_radius}')
print(f'Maximum: {max_radius}')
print(f'Mean: {mean_radius}')
print(f'Median: {median_radius}')
print(f'Standard Deviation: {std_radius}')
print()


# Частота
titles = [star['name'] for star in filtered_items]
label_frequencies = Counter(titles)

for label, frequency in label_frequencies.items():
    print(f'{label}: {frequency}')