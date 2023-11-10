import requests
from bs4 import BeautifulSoup
import pandas as pd
def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        html = ""
        for row in file.readlines():
            html += row
        soup = BeautifulSoup(html, 'html.parser')
        item=dict()
        item['cost'] = soup.find_all(class_="el-cost__current")[0].get_text().strip()
        item['title']=soup.find_all('a', class_="section-product-preview__title-bottom pe-none")[0].get_text().strip()

        return item
handle_file("shop.html")