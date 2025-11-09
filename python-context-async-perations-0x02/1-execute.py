import sqlite3

db_file_path = "user.db"

class ExecuteQuery:

    def __init__(self, query, parameter):
        self.conn = sqlite3.connect(db_file_path)
        self.query = query
        self.parameter = parameter

    def __enter__(self):
        cursor = self.conn.cursor()
        cursor.execute(self.query, (self.parameter,))
        return cursor.fetchone()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.conn.close()
        print(exc_type, exc_value, exc_tb, sep="\n")


with ExecuteQuery("SELECT * FROM user WHERE age > ?", 2) as db_query:
    print(db_query)