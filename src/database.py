import sqlite3


class LiteDatabase:

    def __init__(self):
        self.conn = sqlite3.connect('/Users/jazib/Desktop/workrepo/FAST_Resources_Reverse_Indexer/fast_zakhira.db')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS reverse_index (
                WORD           TEXT    NOT NULL,
                TOPIC_NAME     TEXT    NOT NULL,
                FILE_NAME      TEXT    NOT NULL,
                RELEVANCE INT NOT NULL
            );''')

        self.conn.execute('''
            CREATE INDEX IF NOT EXISTS 
            search_pattern_1 on reverse_index (word, topic_name, relevance);
        ''')

        self.conn.execute('''
            CREATE INDEX IF NOT EXISTS 
            search_pattern_2 on reverse_index (word, relevance);
        ''')
        print("Database ready")

    def insert_index(self, topic_name, file_path, words):
        query = ""
        try:
            for word, relevance in words.items():
                query = "INSERT INTO reverse_index VALUES (?, ?, ?, ?);"
                self.conn.execute(query, [word, topic_name, file_path, relevance])
            self.conn.commit()
        except Exception as e:
            print(e)
            print(query)

    def close(self):
        self.conn.close()

    def search(self, word):
        query = """
        SELECT * FROM reverse_index
        WHERE word like ?
        ORDER BY relevance DESC
        """
        cursor = self.conn.execute(query, [word])
        return {row[2]: row for row in cursor}
