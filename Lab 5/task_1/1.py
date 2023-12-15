import csv
import json
from bson import json_util
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
            item['age'] = int(row[5])
            items1.append(item)
    return items1

file_name1 = "task_1_item.csv"
items1 = decode_csv(file_name1)
#print(decode_csv(file_name1))

def insert_many(collection, items1):
    collection.insert_many(items1)

#insert_many(connect(), items1)

def write_json(file_name1, data):
    with open(file_name1, 'w', encoding='utf-8') as file:
        file.write(json_util.dumps(data, ensure_ascii=False))

# Вывод первых 10 записей, по убыванию по полю salary
def sort_by_salary(collection):
    items = collection.find().limit(10).sort('salary', -1)
    write_json('result_task_1.1.json', items)

sort_by_salary(connect())

# Вывод первых 15 записей, отфильтрованных по предикату age < 30,
# отсортировать по убыванию по полю salary
def sort_by_age(collection):
    # The sorting is passed as a list of tuples, and limit is chained as a cursor method.
    cursor = collection.find({"age": {"$lt": 30}}).sort([("salary", -1)]).limit(15)
    items = list(cursor)  # Convert cursor to list
    write_json('result_task_1.2.json', items)


sort_by_age(connect())
# вывод первых 10 записей, отфильтрованных по сложному предикату: (записи только из произвольного города,
# записи только из трех произвольно взятых профессий), отсортировать по возрастанию по полю age
def sort_by_city_job(collection):
    items = []
    for test in (collection
                 .find({"city": "Тарраса", "job": {"$in": ["Строитель", "Врач", "Программист"]}})
                 .sort('age', 1).limit(10)):  # Fix to sort method
        test["_id"] = str(test["_id"])
        items.append(test)

    write_json('result_task_1.3.json', items)

sort_by_city_job(connect())

# вывод количества записей, получаемых в результате следующей фильтрации (age в
# произвольном диапазоне, year в [2019,2022], 50 000 < salary <= 75 000 || 125 000 < salary < 150 000).
def sort_condition(collection):
    count = collection.count_documents({
        "$and": [
            {"age": {"$gte": 18, "$lte": 65}},
            {"year": {"$in": [2019, 2020, 2021, 2022]}},
            {"$or": [
                {"salary": {"$gt": 50000, "$lte": 75000}},
                {"salary": {"$gt": 125000, "$lt": 150000}}
            ]}
        ]
    })

    with open('result_task_1.4.json', 'w', encoding='utf-8') as file:
        json.dump({"count": count}, file, ensure_ascii=False, indent=4)

sort_condition(connect())
