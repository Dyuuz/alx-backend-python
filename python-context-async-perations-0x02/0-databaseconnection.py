import sqlite3

db_file_path = "user.db"

class DatabaseConnection:

    def __init__(self):
        self.conn = sqlite3.connect(db_file_path)

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.conn.close()
        print(exc_type, exc_value, exc_tb, sep="\n")

with DatabaseConnection() as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())