import pickle
import csv
import json
import sqlite3

def parse_data(file_name1):
    items1 = []
    with open(file_name1, mode='rb') as pkl_f:
        data = pickle.load(pkl_f)
        for item in data:
            if len(item) == 6:
                item['category'] = 'no'
            item['version']=0
            items1.append(item)
    return items1


def decode_csv(file_name2):
    items2 = []
    with open(file_name2, "r", encoding="utf-8") as input:
        reader = csv.reader(input, delimiter=";")
        next(reader)
        for row in reader:
            if len(row) == 0:
                continue
            item = dict()
            item['name'] = row[0]
            item['method'] = row[1]
            if item['method'] == 'available':
                item['param'] = row[2] == "True"
            elif item['method'] != 'remove':
                item['param'] = float(row[2])
            items2.append(item)
    return items2


file_name1 = "task_4_var_58_product_data.pkl"
items1 = parse_data(file_name1)
#print(parse_data(file_name1))



file_name2 = "task_4_var_58_update_data.csv"
items2 = decode_csv(file_name2)
#print(decode_csv(file_name2))


conn = sqlite3.connect('goods.db')
c = conn.cursor()
db = sqlite3.connect('goods.db')
c.execute('''CREATE TABLE IF NOT EXISTS goods 
             (name TEXT, price INTEGER, quantity INTEGER, category TEXT, fromCity TEXT, isAvailable TEXT, views INTEGER, version INTEGER
            )''')


def insert_pickle_data(db, data):
    cursor = db.cursor()
    for item in data:
        item['version'] = 0
    cursor.executemany("""
            INSERT INTO goods (name, price, quantity, category, fromCity, isAvailable, views, version)
            VALUES (
                :name, :price, :quantity, :category, :fromCity, :isAvailable, :views, :version
            )""", data)
    db.commit()


def delete_by_name(db, name):
    cursor = db.cursor()
    cursor.execute("DELETE FROM goods WHERE name = ?", [name])
    db.commit()


def update_price_by_percent(db, name, percent):
    cursor = db.cursor()
    cursor.execute("UPDATE goods SET price = round(price * (1 + ?), 2) WHERE name = ?", [percent, name])
    cursor.execute("UPDATE goods SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def update_price(db, name, param):
    cursor = db.cursor()
    res = cursor.execute("""
     UPDATE goods SET price = (price + ?) WHERE (name = ?) AND ((price + ?) > 0)
     """, [param, name, param])
    if res.rowcount > 0:
        cursor.execute("UPDATE goods SET version = version + 1 WHERE name = ?", [name])
        db.commit()


def update_available(db, name, param):
    cursor = db.cursor()
    cursor.execute("UPDATE goods SET isavailable = ? WHERE name = ?", [param, name])
    cursor.execute("UPDATE goods SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def update_quantity(db, name, param):
    cursor = db.cursor()
    res = cursor.execute("UPDATE goods SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?) > 0)",
                         [param, name, param])
    if res.rowcount > 0:
        cursor.execute("UPDATE goods SET version = version + 1 WHERE name = ?", [name])
        db.commit()


def handle_update(db, update_items):
    for item in update_items:
        match item['method']:
            case 'remove':
                pass
                print(f"Deleting {item['name']}")
                delete_by_name(db, item['name'])
            case 'price_percent':
                print(f"Update price by percent for {item['name']}")
                update_price_by_percent(db, item['name'], item['param'])
            case 'price_abs':
                print(f"Update price absolute value for {item['name']}")
                update_price(db, item['name'], item['param'])
            case 'quantity_sub':
                print(f"Subtract quantity for {item['name']}")
                update_quantity(db, item['name'], item['param'])
            case 'quantity_add':
                print(f"Add quantity for {item['name']}")
                update_quantity(db, item['name'], item['param'])
            case 'available':
                print(f"Update availability for {item['name']}")
                update_available(db, item['name'], item['param'])

handle_update(db, items2)


# Топ 10 самых обновляемых товаров
def top_10(db, limit):
    cursor=db.cursor()
    res = cursor.execute("SELECT name, version FROM goods ORDER BY version DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = {'name': row[0], 'version': row[1]}
        items.append(item)
    cursor.close()

    return items

task_1 = top_10(db,10)

with open('result_task_4.1.json', 'w') as f:
    json.dump(task_1, f, indent=4)

# Проанализировать цены товаров, найдя (сумму, мин, макс, среднее) для каждой группы, а также количество товаров в группе
def price_analysis(db):
    cursor = db.cursor()
    res = cursor.execute("""
            SELECT category,
                ROUND(SUM(price), 2) as sum, 
                ROUND(AVG(price), 2) as avg, 
                MIN(price) as min,
                MAX(price) as max,
                COUNT (*) as count
            FROM goods
            GROUP BY category
            """)
    items = []
    for row in res.fetchall():
        item = {'category': row[0], 'sum': row[1], 'avg': row[2], 'min': row[3], 'max': row[4], 'count': row[5]}
        items.append(item)
    cursor.close()

    return items

task_2=price_analysis(db)

with open('result_task_4.2.json', 'w') as f:
    json.dump(task_2, f, indent=4)

# проанализировать остатки товаров, найдя (сумму, мин, макс, среднее) для каждой группы товаров
def analyse_quant(db):
    cursor=db.cursor()
    res=cursor.execute("""
            SELECT category,
                SUM(quantity) as quantity
            FROM goods
            GROUP BY category
            """)
    items_l = []
    for row in res.fetchall():
        item={'category': row[0], 'sum': row[1]}
        items_l.append(item)
    cursor.close()

    return items_l

task_3=analyse_quant(db)

with open('result_task_4.3.json', 'w') as f:
    json.dump(task_3, f, indent=4)

# Самый дешевый товар в наличии в каждой категории
def available(db, categories):
    cursor = db.cursor()
    result = {}

    for category in categories:
        res = cursor.execute("""
            SELECT name, price
            FROM goods
            WHERE category = ? AND isavailable = 1
            ORDER BY price
        """, [category])
        result[category] = {row[0]: row[1] for row in res.fetchall()}

    cursor.close()
    return result

categories = ["cosmetics", "fruit", "tools"]

task_4 = available(db, categories)

with open('result_task_4.4.json', 'w') as f:
    json.dump(task_4, f, indent=4)


insert_pickle_data(conn, items1)