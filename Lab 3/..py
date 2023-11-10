import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://ekb.bvdshop.ru/"
html=requests.get(url)
print(html.text)

site = BeautifulSoup(text, 'html.parser')
products = site.find_all("div", attrs={'class': 'my-225 col-4'})
for product in products:
    item = dict()
    item['el-cost__current'] = site.find_all("el-cost__current")[0]['src']


    def handle_file(file_name):
        items = list()
        with open(file_name, encoding='utf-8') as file:
            text = ""
            for row in file.readlines():
                text += row