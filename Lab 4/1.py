import sqlite3
import json
def parse_data(file_name):
    items = []
    with open(file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[1:]:
            book_data = line.strip().split(';')

            title = book_data[0]
            author = book_data[1]
            genre = book_data[2]
            pages = int(book_data[3])
            published_year = int(book_data[4])
            isbn = book_data[5]
            rating = float(book_data[6])
            views = int(book_data[7])

            book = {
                'title': title,
                'author': author,
                'genre': genre,
                'pages': pages,
                'published_year': published_year,
                'isbn': isbn,
                'rating': rating,
                'views': views
            }
            items.append(book)

    return items

def connect_to_db(file_name):
    connection= sqlite3.connect(file_name)
    connection.row_factory=sqlite3.Row
    return connection
def insert_data (db,data):
    cursor=db.cursor()
    cursor.executemany("""
        INSERT INTO books (title, author, genre, pages, published_year, isbn, rating, views)
        VALUES(:title, :author, :genre, :pages, 
            :published_year, :isbn, :rating, :views
        )
    """, data)
    db.commit()
items=parse_data("task_1_var_58_item.csv")
db=connect_to_db("books.db")
insert_data(db,items)

result=db.cursor().execute("SELECT * FROM books")
#print(result.fetchall())


# вывод первых (68) отсортированных по произвольному числовому полю строк из таблицы в файл формата json
def get_top_by_views(db, limit):
    cursor = db.cursor()
    res = cursor.execute("select title, author, pages, views from books order by views desc limit ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items

result1 = get_top_by_views(db, 68)

with open('result1.json', 'w') as f:
    json.dump(result1, f, indent=4)

# вывод (сумму, мин, макс, среднее) по произвольному числовому полю;

def get_stat_by_pages(db):
    cursor = db.cursor()
    res = cursor.execute("""
        select
            sum(pages) as sum,
            avg(pages) as avg,
            min(pages) as min,
            max(pages) as max
        from books
        """)
    result2 = dict(res.fetchone())
    cursor.close()

    with open('result2.json', 'w') as f:
        json.dump(result2, f, indent=4)

    return result

result2 = get_stat_by_pages(db)

# вывод частоты встречаемости для категориального поля

def get_freq_by_century(db):
    cursor=db.cursor()
    res=cursor.execute("""
            SELECT
                CAST(count(*)as REAL)/ (SELECT COUNT(*) FROM books) as count,
                (FLOOR (published_year/100)+1) as century
            FROM books
            GROUP BY (FLOOR(published_year/100)+1)
            """)
    result3=[]
    for row in res.fetchall():
        item = dict(row)
        result3.append(item)
    cursor.close()

    with open('result3.json', 'w') as f:
        json.dump(result3, f, indent=4)

    return result3

result3 = get_freq_by_century(db)

# вывод первых (68) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json.
def filter_by_published_year(db,min_published_year, limit=68):
    cursor=db.cursor()
    res=cursor.execute("""
            SELECT *
            FROM books
            WHERE published_year > ?
            ORDER BY views DESC
            LIMIT ?
            """, [min_published_year, limit])
    result4 = []
    for row in res.fetchall():
        item = dict(row)
        result4.append(item)
    cursor.close()
    return result4

result4 = filter_by_published_year(db, 68)

with open('result4.json', 'w') as f:
    json.dump(result4, f, indent=4)