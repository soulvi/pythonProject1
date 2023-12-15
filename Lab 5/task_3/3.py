# -*- coding: utf-8 -*-
import json
import pickle
from pymongo import MongoClient
import math

def connect():
    client=MongoClient()
    db=client['database3']
    return db.test

def decode_pkl(file_name):
    with open(file_name, "rb") as file:
        res = pickle.load(file)
        return res

file_name = "task_3_item.pkl"
items1 = decode_pkl(file_name)
#print(items1)

def insert_many(collection, items1):
    collection.insert_many(items1)

insert_many(connect(), items1)

#Необходимо считать данные и добавить их к той коллекции,
# куда были записаны данные в первом и втором заданиях.

# Удалить из коллекции документы по предикату:
# salary < 25 000 || salary > 175000

def delete_salary(collection):
    result=collection.delete_many({
        "$or": [
            {"salary": {"$lt":25_000}},
            {"salary": {"$gt": 175_000}},
        ]
    })
    print(result)
#delete_salary(connect())

# увеличить возраст (age) всех документов на 1
def update_age(collection):
    result=collection.update_many({}, {
        "$inc":{
            "age":1}
    })
    print(result)
#update_age(connect())

# поднять заработную плату на 5% для произвольно выбранных профессий
def increase_salary_by_job(collection):
    filter={
        "job":{"$in":["Учитель", "Врач","Строитель","Повар"]}
    }
    update={
        "$mul": {
            "salary": 1.05
        }
    }
    result=collection.update_many(filter, update)
    print(result)
#increase_salary_by_job(connect())

# поднять заработную плату на 7% для произвольно выбранных городов
def increase_salary_by_city(collection):
    filter={
        "city":{"$in":["Баку", "Луго","Эльче","Душанбе"]}
    }
    update={
        "$mul": {
            "salary": 1.07
        }
    }
    result=collection.update_many(filter, update)
    print(result)
# "$nin - все, кроме перечисленнных городов
#increase_salary_by_city(connect())

# поднять заработную плату на 10% для выборки по сложному предикату
# (произвольный город, произвольный набор профессий, произвольный диапазон возраста)
def increase_salary(collection):
    filter={
        "city":{"$nin":["Баку", "Луго","Эльче","Душанбе"]},
        "job":{"$in":["Врач", "Строитель", "Учитель", "Бухгалтер"]},
        "age":{"$gt":18, "$lt":45}
    }
    update={
        "$mul": {
            "salary": 1.1
        }
    }
    result=collection.update_many(filter, update)
    print(result)
#increase_salary(connect())

# удалить из коллекции записи по произвольному предикату
def delete_year(collection):
    result=collection.delete_many({
        "year":{"$in":[2005,2006,2007]
                }
        }
    )
    print(result)
delete_year(connect())