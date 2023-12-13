import sqlite3
import json
import csv
import xlrd
def decode_csv(file_name1):
    items1 = []
    with open(file_name1, "r", encoding="utf-8") as input:
        reader = csv.reader(input, delimiter=",")
        next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            item = dict()
            item['id'] = int(row[0])
            item['gender'] = row[1]
            item['masterCategory']=row[2]
            item['subCategory']=row[3]
            item['articleType']=row[4]
            item['baseColor']=row[5]
            item['season']=row[6]
            item['year']=row[7]
            item['usage']=row[8]
            item['productDisplayName']=row[9]
            items1.append(item)
    return items1

file_name1 = "styles.csv"
items1 = decode_csv(file_name1)
#print(items1)

def decode_xls(file_name2):
    items2 = []
    workbook = xlrd.open_workbook(file_name2)
    sheet = workbook.sheet_by_index(0)
    for row in range(1, sheet.nrows):
        item = {}
        item['product_id'] = sheet.cell_value(row, 0)
        item['product_name'] = sheet.cell_value(row, 1)
        item['gender'] = sheet.cell_value(row, 2)
        item['category'] = sheet.cell_value(row, 3)
        item['pattern'] = sheet.cell_value(row, 4)
        item['color'] = sheet.cell_value(row, 5)
        item['age_group'] = sheet.cell_value(row, 6)
        item['season'] = sheet.cell_value(row, 7)
        item['price'] = sheet.cell_value(row, 8)
        item['material'] = sheet.cell_value(row, 9)
        items2.append(item)
    return items2


file_name2 = "fashion_data_2018_2022.xls"
items2 = decode_xls(file_name2)
#print(items2)

def decode_json (file_name3):
    with open(file_name3, "r") as json_file:
        json_data = json.load(json_file)
    return json_data


file_name3 = "products.json"
items3= decode_json(file_name3)
#print(items3)

conn = sqlite3.connect('clothing.db')
cur = conn.cursor()


cur.execute('''CREATE TABLE IF NOT EXISTS dataset1 (
                id INTEGER PRIMARY KEY,
                gender TEXT,
                masterCategory TEXT,
                subCategory TEXT,
                articleType TEXT,
                baseColor TEXT,
                season TEXT,
                year INTEGER,
                usage TEXT,
                productDisplayName TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS dataset2 (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT,
                gender TEXT,
                category TEXT,
                pattern TEXT,
                color TEXT,
                age_group TEXT,
                season TEXT,
                price FLOAT,
                material TEXT)''')


cur.execute('''
    CREATE TABLE IF NOT EXISTS dataset3 (
        id INTEGER,
        title TEXT,
        price REAL,
        description TEXT,
        category TEXT
    )
''')

def insert_data(items1, items2, items3):
    for item in items1:
        cur.execute('''
            INSERT INTO dataset1 ( gender, masterCategory, subCategory, articleType, baseColor,
            season, year, usage, productDisplayName) 
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            ( item['gender'], item['masterCategory'], item['subCategory'], item['articleType'],
            item['baseColor'], item['season'], item['year'], item['usage'], item['productDisplayName']))

    for item in items2:
        cur.execute('''
            INSERT INTO dataset2 (product_name, gender, category, pattern, color,
            age_group, season, price, material) values ( ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            ( item['product_name'], item['gender'], item['category'], item['pattern'],
            item['color'], item['age_group'], item['season'], item['price'], item['material']))

    for item in items3:
        cur.execute('''
            INSERT INTO dataset3 (id, title, price, description, category) values (?, ?, ?, ?, ?)''',
            ( item['id'], item['title'], item['price'], item['description'], item['category']))

    conn.commit()

insert_data(items1, items2, items3)


# вывод первых (68) отсортированных по цене строк
def clothing_1(db, limit):
    cursor = db.cursor()
    cursor.execute("SELECT product_name, gender, category, age_group, price FROM dataset2 ORDER BY price DESC LIMIT ?", [limit])
    rows = cursor.fetchall()
    items = []
    for row in rows:
        item = {
            "product_name": row[0],
            "gender": row[1],
            "category": row[2],
            "age-group": row[3],
            "price":row[4]
        }
        items.append(item)
    cursor.close()
    return items

query_1 = clothing_1(conn, 68)


with open('result_task_5.1.json', 'w') as f:
    json.dump(query_1, f, indent=4)

# Анализ цены товаров в каждой уникальной категории
def clothing_2(db):
    cursor = db.cursor()
    res = cursor.execute("""
            SELECT category,
                ROUND(SUM(price), 2) as sum, 
                ROUND(AVG(price), 2) as avg, 
                MIN(price) as min,
                MAX(price) as max,
                COUNT (*) as count
            FROM dataset2
            GROUP BY category
            """)
    items = []
    for row in res.fetchall():
        item = {'category': row[0], 'sum': row[1], 'avg': row[2], 'min': row[3], 'max': row[4], 'count': row[5]}
        items.append(item)
    cursor.close()

    return items

query_2=clothing_2(conn)

with open('result_task_5.2.json', 'w') as f:
    json.dump(query_2, f, indent=4)

# Вывод количества одежды для каждой гендерной категории
def clothing_3(db):
    cursor=db.cursor()
    res=cursor.execute("""
            SELECT gender,
            COUNT(gender) as count
            FROM dataset1
            GROUP BY gender
            ORDER BY count
            DESC
            """)
    items=[]
    for row in res.fetchall():
        item = {'gender': row[0], 'count':row[1]}
        items.append(item)
    cursor.close()
    return items

query_3=clothing_3(conn)

with open('result_task_5.3.json', 'w') as f:
    json.dump(query_3, f, indent=4)


# Вывод самых дорогих товаров в категории в каждом сезоне
def clothing_4(db):
    cursor = db.cursor()
    cursor.execute("""
            SELECT season, category, product_name, price
            FROM dataset2
            WHERE (price, season) IN (
                SELECT max(price), season FROM dataset2 WHERE season = 'Spring' UNION
                SELECT max(price), season FROM dataset2 WHERE season = 'Summer' UNION
                SELECT max(price), season FROM dataset2 WHERE season = 'Autumn' UNION
                SELECT max(price), season FROM dataset2 WHERE season = 'Winter' UNION
                SELECT max(price), null FROM dataset2
            )
            ORDER BY season, category, price
            """)
    rows = cursor.fetchall()
    items = []
    for row in rows:
        item = {
            "season": row[0],
            "category": row[1],
            "product_name": row[2],
            "price": row[3]
        }
        items.append(item)
    cursor.close()
    return items

expensive_items = clothing_4(conn)

with open('result_task_5.4.json', 'w') as f:
    json.dump(expensive_items, f, indent=4)


# Вывод количества вещей по каждой возрастной категории
def clothing_5(db):
    cursor=db.cursor()
    res=cursor.execute("""
            SELECT age_group, COUNT(*) AS count
            FROM dataset2
            GROUP BY age_group
            ORDER BY count DESC     
            
            """)
    items = []
    for row in res.fetchall():
        item = {'age_group': row[0], 'count': row[1]}
        items.append(item)
    cursor.close()
    return items


query_5 = clothing_5(conn)

with open('result_task_5.5.json', 'w') as f:
    json.dump(query_5, f, indent=4)


# Вывод количества вещей в каждой категории для 3 датасета
def clothing_6(db):
    cursor=db.cursor()
    res=cursor.execute("""
            SELECT category, 
            COUNT(category) AS count
            FROM dataset3
            GROUP BY category
            ORDER BY count DESC     
            
            """)
    items = []
    for row in res.fetchall():
        item = {'category': row[0], 'count': row[1]}
        items.append(item)
    cursor.close()
    return items


query_6 = clothing_6(conn)

with open('result_task_5.6.json', 'w') as f:
    json.dump(query_6, f, indent=4)


# Вывод информации по категории Shoes по двум таблицам
def clothing_7(db):
    cursor=db.cursor()
    res=cursor.execute("""
            SELECT dataset1.subCategory, dataset1.articleType, dataset1.baseColor, dataset2.category, dataset2.price
            FROM dataset1 JOIN dataset2
            ON dataset1.subCategory=dataset2.category
            WHERE dataset2.category="Shoes"
            ORDER BY dataset2.price DESC
            LIMIT 10
            """)
    items=[]
    for row in res.fetchall():
        item={'subcategory':row[0], 'articleType':row[1], 'baseColor':row[2], 'category':row[3], 'price':row[4]}
        items.append(item)
        cursor.close()
        return items

query_7=clothing_7(conn)

with open('result_task_5.7.json', 'w') as f:
    json.dump(query_7, f, indent=4)
