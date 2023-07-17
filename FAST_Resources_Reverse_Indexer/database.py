import sqlite3

def create_table():
    conn = sqlite3.connect('reverse_index.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reverse_index (
            word TEXT PRIMARY KEY,
            files TEXT
        )
    ''')

    conn.commit()
    conn.close()
