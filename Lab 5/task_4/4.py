import csv
import json
from pymongo import MongoClient

def connect():
    client = MongoClient()
    db = client["database4"]
    return db.test

def decode_csv(file_name1):
    items1 = []
    with open(file_name1, "r", encoding="cp1251") as input:
        reader = csv.reader(input, delimiter=",")
        next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            item = dict()
            item['movie_title'] = row[0]
            item['release_date'] = row[1]
            item['genre'] = row[2]
            item['mpaa_rating'] = row[3]
            item['total_gross'] = int(row[4])
            item['inflation_adjusted_gross'] = row[5]
            items1.append(item)
    return items1

file_name1 = "disney_movies.csv"
items1 = decode_csv(file_name1)
#print(items1)


def decode_json(file_name2):
    with open(file_name2, "r", encoding="cp1251") as file:
        result = json.load(file)
    return result

file_name2 = "csvjson.json"
items2 = decode_json(file_name2)
#print(items2)

def insert_many(collection, data):
    collection.insert_many(data)
data=decode_csv("disney_movies.csv")+decode_json("csvjson.json")
#insert_many(connect(),data)

# вывод первых 10 записей, отфильтрованных по: жанру и двум произвольно взятым рейтингам
# отсортировать по убыванию по полю total gross
def sort_by_genre_rating(collection):
    items=[]
    for test in (collection
        .find({"genre":"Musical",
        "mpaa_rating":{"$in": ["G", "PG"]}
        }, limit=10)
        .sort({'total_gross':-1})):
        test["_id"] = str(test["_id"])
        items.append(test)

    with open("result_task_4.1.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

sort_by_genre_rating(connect())

# вывод минимального, среднего, максимального total_gross по жанрам
def stat_by_genre_gross(collection):
    items = []
    q = [
        {
            "$group": {
                "_id": "$genre",
                "max": {"$max": "$total_gross"},
                "min": {"$min": "$total_gross"},
                "avg": {"$avg": "$total_gross"}
            }
        }
    ]

    for stat in collection.aggregate(q):
        items.append(stat)

    return items

task2=stat_by_genre_gross(connect())

with open('result_task_4.2.json', 'w') as f:
    json.dump(task2, f, indent=4, ensure_ascii=False)
# Возможно avg выводится как null, потому что в датасете
# отсутствуют значения total_gross для определенных жанров

# вывод минимального, среднего, максимального total_gross по рейтингу,
# отсортировать вывод по любому полю.
def stat_condition1(collection):
    items = []
    q = [

        {"$group":{
            "_id": "$mpaa_rating",
            "max": {"$max": "$total_gross"},
            "min": {"$min": "$total_gross"},
            "avg": {"$avg": "$total_gross"}
            }
        },
        {"$sort": {
            "total_gross": -1
            }
        }
    ]

    for stat in collection.aggregate(q):
        items.append(stat)

    return items

task3=stat_condition1(connect())

with open('result_task_4.3.json', 'w') as f:
    json.dump(task3, f, indent=4, ensure_ascii=False)

# Удалить из коллекции документы по предикату:
# total_gross < 10000000 || salary > 90000000

def delete_gross(collection):
    result=collection.delete_many({
        "$or": [
            {"total_gross": {"$lt":10000000}},
            {"salary": {"$gt": 90000000}},
        ]
    })
    print(result)
#delete_gross(connect())


def convert_gross_to_numbers(collection):
    documents_with_string_gross = collection.find({
        "total_gross": {"$type": "string"}
    })

    for doc in documents_with_string_gross:
        try:
            collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {"total_gross": int(doc["total_gross"])}}
            )
        except ValueError:
            print(f"Значение {doc['_id']} не подходит'.")

#convert_gross_to_numbers(connect())

# уменьшить total_gross всех документов на 100
def update_gross(collection):
    result=collection.update_many({}, {
        "$inc":{
            "total_gross":-100}
    })
    print(result)
#update_gross(connect())


# Удалить пустые значения "" в жанрах
def delete_empty(collection):
    result=collection.delete_many({
        "genre": ""}
    )
    print(result)
#delete_empty(connect())
