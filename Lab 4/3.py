import msgpack
import csv
import json
import sqlite3

def decode_msgpack(file_name):
    items = []
    with open(file_name, "rb") as file:
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
            items.append(songs)

    return items


def decode_csv(file_name):
    items = []
    with open(file_name, "r", encoding="utf-8") as input:
        reader = csv.reader(input, delimiter=";")
        next(reader)
        for row in reader:
            if len(row) == 0:continue
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
            
            items.append(item)
    return items


file_name1 = "task_3_var_58_part_1.msgpack"
items1 = decode_msgpack(file_name1)
#print(items1)

file_name2 = "task_3_var_58_part_2.csv"
items2 = decode_csv(file_name2)
#print(items2)