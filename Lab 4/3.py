import msgpack
import csv
import json
import sqlite3

def decode_msgpack(file_name1):
    with open(file_name1, 'rb') as f:
        songs_msgpack = msgpack.load(f)

    for song in songs_msgpack:
        del song['mode'], song['speechiness'], song['acousticness'], song['instrumentalness']

    return songs_msgpack


def decode_csv(file_name2):
    with open(file_name2, "r", encoding="utf-8") as file:
        songs_csv = csv.DictReader(file, delimiter=';') 

        items2 = []
        for song in songs_csv:
            del song['energy'], song['key'], song['loudness']
            items2.append(song)

    return items2

file_name1 = "task_3_var_58_part_1.msgpack"
items1 = decode_msgpack(file_name1)

file_name2 = "task_3_var_58_part_2.csv"
items2 = decode_csv(file_name2)

conn = sqlite3.connect('music.db')
c = conn.cursor()
db = sqlite3.connect('music.db')
c.execute('''create table if not exists music 
             (artist text, song text, duration_ms integer, year integer, tempo real, genre text)''')

def insert_msgpack_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
            insert into music (artist, song, duration_ms, year, tempo, genre)
            values (
                :artist, :song, :duration_ms, :year, :tempo, :genre
            )""", data)
    db.commit()

def insert_csv_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
            insert into music (artist, song, duration_ms, year, tempo, genre)
            values (
                :artist, :song, :duration_ms, :year, :tempo, :genre
            )""", data)
    db.commit()

insert_msgpack_data(conn, items1)
insert_csv_data(conn, items2)
# вывод первых (68) отсортированных по произвольному числовому полю строк из таблицы в файл формата json
def get_long_by_duration(db, limit):
    cursor = db.cursor()
    cursor.execute("SELECT artist, song, year, genre FROM music ORDER BY duration_ms DESC LIMIT ?", [limit])
    rows = cursor.fetchall()
    items = []
    for row in rows:
        item = {
            "artist": row[0],
            "song": row[1],
            "year": row[2],
            "genre": row[3]
        }
        items.append(item)
    cursor.close()
    return items

items = get_long_by_duration(conn, 68)
with open('result_task_3.1.json', 'w') as f:
    json.dump(items, f, indent=4,ensure_ascii=False)

# вывод (сумму, мин, макс, среднее) по произвольному числовому полю
def get_stat(db):
    cursor = db.cursor()
    cursor.execute("""
        SELECT
            SUM(tempo) AS sum,
            AVG(tempo) AS avg,
            MIN(tempo) AS min,
            MAX(tempo) AS max
        FROM music
        """)

    fields = [desc[0] for desc in cursor.description]
    values = cursor.fetchone()

    result2_2 = dict(zip(fields, values))
    cursor.close()

    with open('result_task_3.2.json', 'w') as f:
        json.dump(result2_2, f, indent=4, ensure_ascii=False)

    return result2_2

result2 = get_stat(db)

# вывод частоты встречаемости для категориального поля
def freq(db):
    cursor = db.cursor()
    cursor.execute("""
        SELECT genre, COUNT(*) as count
        FROM music
    """)

    fields = [desc[0] for desc in cursor.description]
    values = cursor.fetchone()

    result2_3 = dict(zip(fields, values))
    cursor.close()

    with open('result_task_3.3.json', 'w') as f:
        json.dump(result2_3, f, indent=4,ensure_ascii=False)

    return result2_3


result2_3 = freq(db)

# вывод первых (68) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json.
def filter_by_year(db, min_year, limit=68):
    cursor = db.cursor()
    res = cursor.execute("""
            select *
            from music
            where year > ?
            order by duration_ms desc
            limit ?
            """, [min_year, limit])
    fields = [desc[0] for desc in cursor.description]
    values = cursor.fetchall()

    result = [dict(zip(fields, row)) for row in values]
    cursor.close()

    with open('result_task_3.4.json', 'w') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    return result


result = filter_by_year(db, 68)
