import json
from pymongo import MongoClient
import math

def connect():
    client=MongoClient()
    db=client['database2']
    return db.test

def decode_txt(file_name):
    items = list()
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        item = dict()
        for line in lines:
            if line.strip() == '=====':
                items.append(item)
                item = dict()
            else:
                line = line.strip()
                splitted = line.split('::')
                if len(splitted) == 2:
                    if splitted[0] in ['id', 'year', 'age']:
                        item[splitted[0]] = int(splitted[1])
                    elif splitted[0] == 'salary':
                        item[splitted[0]] = float(splitted[1])
                    else:
                        item[splitted[0]] = splitted[1]

    return items

file_name = "task_2_item.text"
items1 = decode_txt(file_name)
#print(items1)

def insert_many(collection, items1):
    collection.insert_many(items1)

#insert_many(connect(), items1)

# вывод минимальной, средней, максимальной salary
def get_stat_by_salary(collection):
    items=[]
    q = [
        {
            "$group": {
                "_id": "result",
                "max": {"$max": "$salary"},
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"}
            }
        }
    ]

    for stat in collection.aggregate(q):
        stat["avg"] = round(stat["avg"], 2)
        items.append(stat)

    return items

task1=get_stat_by_salary(connect())

with open('result_task_2.1.json', 'w') as f:
    json.dump(task1, f, indent=4)


# вывод количества данных по представленным профессиям
def count_by_job(collection):
    items = []
    q = [
        {
            "$group": {
                "_id": "$job",
                "count":{"$sum":1}
            }
        },
        {
            "$sort":{
            "count":-1
            }
        }
    ]

    for stat in collection.aggregate(q):
        items.append(stat)

    return items

task2=count_by_job(connect())

with open('result_task_2.2.json', 'w') as f:
    json.dump(task2, f, indent=4, ensure_ascii=False)



# вывод минимальной, средней, максимальной salary по городу
def stat_by_salary_city(collection):
    items = []
    q = [
        {
            "$group": {
                "_id": "$city",
                "max": {"$max": "$salary"},
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"}
            }
        }
    ]

    for stat in collection.aggregate(q):
        stat["avg"] = round(stat["avg"], 2)
        items.append(stat)

    return items

task3=stat_by_salary_city(connect())

with open('result_task_2.3.json', 'w') as f:
    json.dump(task3, f, indent=4, ensure_ascii=False)

# вывод минимальной, средней, максимальной salary по профессии
def stat_by_job(collection):
    items = []
    q = [
        {
            "$group": {
                "_id": "$job",
                "max": {"$max": "$salary"},
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"}
            }
        }
    ]

    for stat in collection.aggregate(q):
        stat["avg"] = round(stat["avg"], 2)
        items.append(stat)

    return items

task4=stat_by_job(connect())

with open('result_task_2.4.json', 'w') as f:
    json.dump(task4, f, indent=4, ensure_ascii=False)

# вывод минимального, среднего, максимального возраста по городу
def stat_by_age_city(collection):
    items = []
    q = [
        {
            "$group": {
                "_id": "$city",
                "max": {"$max": "$age"},
                "min": {"$min": "$age"},
                "avg": {"$avg": "$age"}
            }
        }
    ]

    for stat in collection.aggregate(q):
        stat["avg"] = math.ceil(stat["avg"])
        items.append(stat)

    return items

task5=stat_by_age_city(connect())

with open('result_task_2.5.json', 'w') as f:
    json.dump(task5, f, indent=4, ensure_ascii=False)

# вывод минимального, среднего, максимального возраста по профессии

def stat_by_age_job(collection):
    items = []
    q = [
        {
            "$group": {
                "_id": "$job",
                "max": {"$max": "$age"},
                "min": {"$min": "$age"},
                "avg": {"$avg": "$age"}
            }
        }
    ]

    for stat in collection.aggregate(q):
        stat["avg"] = math.ceil(stat["avg"])
        items.append(stat)

    return items

task6=stat_by_age_job(connect())

with open('result_task_2.6.json', 'w') as f:
    json.dump(task6, f, indent=4, ensure_ascii=False)

# вывод максимальной заработной платы при минимальном возрасте
def max_salary_min_age(collection):
    items = []
    q = [
        {
            "$group": {
                "_id": "age",
                "age": {"$min": "$age"},
                "max_salary": {"$max": "$salary"}
            }
        },
        {"$match":{"age":18}}
    ]

    for stat in collection.aggregate(q):
        items.append(stat)

    return items
   # q=[
    #     {
    #         "$group":{
    #             "_id":"$age",
    #             "min_salary":{"$min":"salary"}
    #         }
    #     },
    #     {
    #         "$group":{
    #             "_id":"result",
    #             "max_age":{"$max":"$_id"},
    #             "min_salary":{"$min":"$min_salary"}
    #         }
    #     }
    # ]
task7=max_salary_min_age(connect())

with open('result_task_2.7.json', 'w') as f:
    json.dump(task7, f, indent=4, ensure_ascii=False)

# вывод минимальной заработной платы при максимальной возрасте
def min_salary_max_age(collection):
    items = []
    q = [
        {
            "$group": {
                "_id": "age",
                "age": {"$max": "$age"},
                "min_salary": {"$min": "$salary"}
            }
        },
        {"$match":{"age":65}}
    ]

    for stat in collection.aggregate(q):
        items.append(stat)

    return items

task8=min_salary_max_age(connect())

with open('result_task_2.8.json', 'w') as f:
    json.dump(task8, f, indent=4, ensure_ascii=False)

# вывод минимального, среднего, максимального возраста по городу,
# при условии, что заработная плата больше 50 000, отсортировать вывод по любому полю.
def stat_condition1(collection):
    items = []
    q = [
        {
            "$match": {
                "salary": {"$gt": 50000},
            }
        },
        {"$group":{
            "_id": "$city",
            "max_age": {"$max": "$age"},
            "min_age": {"$min": "$age"},
            "avg_age": {"$avg": "$age"}
            }
        },
        {"$sort": {
            "avg_age": -1
            }
        }
    ]

    for stat in collection.aggregate(q):
        stat["avg_age"] = math.ceil(stat["avg_age"])
        items.append(stat)

    return items

task9=stat_condition1(connect())

with open('result_task_2.9.json', 'w') as f:
    json.dump(task9, f, indent=4, ensure_ascii=False)

# вывод минимальной, средней, максимальной salary в произвольно заданных диапазонах
# по городу, профессии,и возрасту: 18<age<25 & 50<age<65

def stat_condition2(collection):
    items = []
    q = [
        {
            "$match": {
                "city": {"$in": ["Хихон","Ереван","Афины", "Загреб"]},
                "job": {"$in":["Врач", "Повар", "Учитель","Инженер"]},
                "$or":[
                    {"age":{"$gt":18, "$lt":25}},
                    {"age":{"$gt":50, "$lt":65}},
                ]
            }
        },
        {"$group":{
            "_id": "result",
            "max": {"$max": "$salary"},
            "min": {"$min": "$salary"},
            "avg": {"$avg": "$salary"}
            }
        }
    ]

    for stat in collection.aggregate(q):
        stat["avg"] = round(stat["avg"], 2)
        items.append(stat)

    return items

task10=stat_condition2(connect())

with open('result_task_2.10.json', 'w') as f:
    json.dump(task10, f, indent=4, ensure_ascii=False)

# вывод минимального, среднего, максимального возраста по году в произвольно заданных диапазонах
# по городу, профессии, при условии, что заработная плата больше 100 000, отсортировать вывод по любому полю.
def stat_condition3(collection):
    items = []
    q = [
        {
            "$match": {
                "salary": {"$gt": 100000},
                "city": {"$in": ["Хихон", "Ереван", "Афины", "Загреб"]},
                "job": {"$in": ["Врач", "Повар", "Учитель", "Инженер"]},
            }
        },
        {"$group":{
            "_id": "$year",
            "max_age": {"$max": "$age"},
            "min_age": {"$min": "$age"},
            "avg_age": {"$avg": "$age"}
            }
        },
        {"$sort": {
            "year": -1
            }
        }
    ]

    for stat in collection.aggregate(q):
        stat["avg_age"] = math.ceil(stat["avg_age"])
        items.append(stat)

    return items

task11=stat_condition3(connect())

with open('result_task_2.11.json', 'w') as f:
    json.dump(task11, f, indent=4, ensure_ascii=False)
