import sqlite3
from reverse_index import build_reverse_index

repo_path = '/content/FAST-Resources'

build_reverse_index(repo_path)

conn = sqlite3.connect('reverse_index.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM reverse_index')

rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()

conn = sqlite3.connect('reverse_index.db')
cursor = conn.cursor()

search_term = 'DemandPaging'

cursor.execute("SELECT * FROM reverse_index WHERE word LIKE '%' || ? || '%'", (search_term,))

rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
