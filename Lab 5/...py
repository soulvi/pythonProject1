import csv
import json
from pymongo import MongoClient


def connect():
    client = MongoClient()
    db = client["test_database"]
    return db.test

def decode_csv(file_name1):
    items1 = []
    with open(file_name1, "r", encoding="utf-8") as input:
        reader = csv.reader(input, delimiter=";")
        next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            item = dict()
            item['job'] = row[0]
            item['salary'] = int(row[1])
            item['id'] = row[2]
            item['city'] = row[3]
            item['year'] = row[4]
            item['age'] = row[5]
            items1.append(item)
    return items1

file_name1 = "task_1_item.csv"
items1 = decode_csv(file_name1)
#print(decode_csv(file_name1))

def insert_many(collection, items1):
    collection.insert_many(items1)

#insert_many(connect(), items1)

# Вывод первых 10 записей, по убыванию по полю salary
def sort_by_salary(collection):
    items = []
    for test in collection.find({}, limit=10).sort({"salary": -1}):
        test["_id"] = str(test["_id"])
        items.append(test)

    with open("task1_1.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

sort_by_salary(connect())


# Вывод первых 15 записей, отфильтрованных по предикату age < 30, отсортировать по убыванию по полю salary
def sort_by_age(collection):
    for test in collection.find({"age": {"$lt": 30}}, limit=15).sort([("salary", -1)]):
        print(test)



sort_by_age(connect())


# вывод первых 10 записей, отфильтрованных по сложному предикату: (записи только из произвольного города,
# записи только из трех произвольно взятых профессий), отсортировать по возрастанию по полю age
def sort_by_city_job(collection):
    items=[]
    for test in (collection
        .find({"city":"Тарраса",
        "job":{"$in": ["Строитель", "Врач", "Программист"]}
        }, limit=10)
        .sort({'age':1})):
        test["_id"] = str(test["_id"])
        items.append(test)

    with open("task1_3.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))

sort_by_city_job(connect())

# вывод количества записей, получаемых в результате следующей фильтрации (age в
# произвольном диапазоне, year в [2019,2022], 50 000 < salary <= 75 000 || 125 000 < salary < 150 000).
def count_object(collection):
    result = collection.count_documents({
        'age': {"$gte": 31, "$lte": 46},
        'year': {"$gte": 2019, "$lte": 2022},
        '$or': [
            {'salary': {'$gt': 50000, '$lt': 75000}},
            {'salary': {'$gt': 125000, '$lt': 150000}}, ]

    })
    # print(result)
    write_result_to_json(result, 'count_object.json')
count_object(connect())




