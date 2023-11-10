from bs4 import BeautifulSoup
import re
import json
import numpy as np
from collections import Counter

def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text=""
        for row in file.readlines():
            text+=row
        items=[]
        site=BeautifulSoup(text, 'html.parser')
        #print(site.prettify())
        item=dict()
        item['class']=site.find_all("span", string=re.compile("Категория:"))[0].get_text().split(":")[1].strip()
        item['title']=site.find_all("h1")[0].get_text().strip()
        item['author']=site.find_all("p")[0].get_text().strip()
        item['pages']=site.find_all("span", attrs={'class': 'pages'})[0].get_text().split(":")[1].strip()
        item['year']=site.find_all("span", attrs={'class':'year'})[0].get_text().split("в")[1].strip()
        item['isbn']=site.find_all("span", string=re.compile("ISBN:"))[0].get_text().split(":")[1].strip()
        item['description']=site.find_all("p")[1].get_text().replace("Описание", "").strip()
        item['img_url']=site.find_all("img")[0]['src']
        item['rating']=float(site.find_all("span", string=re.compile("Рейтинг:"))[0].get_text().split(":")[1].strip())
        item['views']=int(site.find_all("span", string=re.compile("Просмотры:"))[0].get_text().split(":")[1].strip())

        return item

handle_file("1/58.html")
items=[]
for i in range(1,999):
    file_name=f"1/{i}.html"
    result=handle_file(file_name)
    items.append(result)
items=sorted(items, key=lambda x: x['views'], reverse=True)

with open("results_all_1.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items))

filtered_items=[]
for book in items:
    if book['rating']>=4.5:
        filtered_items.append(book)

print(len(items))
print(len(filtered_items))
print()
# Список значений поля "views"
views = [book['views'] for book in items]

total_views = np.sum(views)
min_views = np.min(views)
max_views = np.max(views)
mean_views = np.mean(views)
median_views = np.median(views)
std_views = np.std(views)

print('Views:')
print(f'Total: {total_views}')
print(f'Minimum: {min_views}')
print(f'Maximum: {max_views}')
print(f'Mean: {mean_views}')
print(f'Median: {median_views}')
print(f'Standard Deviation: {std_views}')
print()


# Частота
titles = [book['title'] for book in filtered_items]
label_frequencies = Counter(titles)

for label, frequency in label_frequencies.items():
    print(f'{label}: {frequency}')