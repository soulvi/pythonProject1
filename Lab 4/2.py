import msgpack
import sqlite3
import json

def load_data(file_name):
    items = []
    with open(file_name, "rb") as file:
        decoded_data = file.read()
        data = msgpack.unpackb(decoded_data)

        for row in data[1:]:
            title = row['title']
            price = row['price']
            place = row['place']
            date = row['date']

            book2 = {
                'title': title,
                'price': price,
                'place': place,
                'date': date
            }
            items.append(book2)

    return items


file_name = "task_2_var_58_subitem.msgpack"
items = load_data(file_name)


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection


def insert_additional_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
            INSERT INTO database (books_id, price, place, date)
            VALUES (
                (SELECT id FROM books WHERE title = :title),
                :price, :place, :date
            )""", data)
    db.commit()

# Вся информация по книгам "451 градус по Фаренгейту"
def first_query(db, title):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * 
        FROM database 
        WHERE books_id = (SELECT id FROM books WHERE title = ?)
        """, [title])
    items = []
    for row in res.fetchall():
        item = dict(row)
        print(item)

    cursor.close()
    return items
#Значения по полю price
def second_query(db, title):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            AVG(price) as avg_price, 
            MAX(price) as max_price,
            MIN(price) as min_price
        FROM database 
        WHERE books_id = (SELECT id FROM books WHERE title = ?)
        """, [title])
    print(dict(res.fetchone()))

    cursor.close()
    return []

# Сколько книг с одноименным заголовком существует в таблице?
def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT title, COUNT(*) as count
        FROM books
        GROUP BY title
        HAVING count > 1
    """,)

    items=[]
    for row in res.fetchall():
        item=dict(row)
        print(item)

    cursor.close()
    return items

#items=load_data("task_2_var_58_subitem.msgpack")
db = connect_to_db("books.db")
#insert_additional_data(db,items)
third_query(db)
