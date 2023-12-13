import msgpack
import csv
import json
import sqlite3

def decode_msgpack(file_name1):
    items1 = []
    with open(file_name1, "rb") as file:
        decoded_data = file.read()
        data = msgpack.unpackb(decoded_data)
        for row in data[1:]:
            artist = row['artist']
            song = row['song']
            duration_ms = row['duration_ms']
            year = row['year']
            tempo = row['tempo']
            genre = row['genre']
            mode = row['mode']
            speechiness = row['speechiness']
            acousticness = row['acousticness']
            instrumentalness = row['instrumentalness']

            songs = {
                'artist': artist,
                'song': song,
                'duration_ms': duration_ms,
                'year': year,
                'tempo': tempo,
                'genre': genre,
                'mode': mode,
                'speechiness': speechiness,
                'acousticness': acousticness,
                'instrumentalness': instrumentalness
            }
            items1.append(songs)

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
            item['artist'] = row[0]
            item['song'] = row[1]
            item['duration_ms'] = row[2]
            item['year'] = row[3]
            item['tempo'] = row[4]
            item['genre'] = row[5]
            item['energy'] = row[6]
            item['key'] = row[7]
            item['loudness'] = row[8]

            items2.append(item)
    return items2

file_name1 = "task_3_var_58_part_1.msgpack"
items1 = decode_msgpack(file_name1)

file_name2 = "task_3_var_58_part_2.csv"
items2 = decode_csv(file_name2)

conn = sqlite3.connect('music.db')
c = conn.cursor()
db = sqlite3.connect('music.db')
c.execute('''create table if not exists music 
             (artist text, song text, duration_ms integer, year integer, tempo real, genre text, mode integer, speechiness real,
             acousticness real, instrumentalness real)''')

def insert_msgpack_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
            insert into music (artist, song, duration_ms, year, tempo, genre, mode, speechiness, acousticness, instrumentalness)
            values (
                :artist, :song, :duration_ms, :year, :tempo, :genre, :mode, :speechiness, :acousticness, :instrumentalness
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
    json.dump(items, f, indent=4)

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
        json.dump(result2_2, f, indent=4)

    return result2_2

result2 = get_stat(db)

# вывод частоты встречаемости для категориального поля
def freq(db):
    cursor = db.cursor()
    cursor.execute("""
        SELECT mode, COUNT(*) as count
        FROM music
    """)

    fields = [desc[0] for desc in cursor.description]
    values = cursor.fetchone()

    result2_3 = dict(zip(fields, values))
    cursor.close()

    with open('result_task_3.3.json', 'w') as f:
        json.dump(result2_3, f, indent=4)

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
        json.dump(result, f, indent=4)

    return result


result = filter_by_year(db, 68)