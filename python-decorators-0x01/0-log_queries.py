import sqlite3
import functools
from datetime import datetime

def connect_to_db():
    conn = sqlite3.connect("user.db")
    return conn

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else args[0] if args else "UNKNOWN QUERY"
        date = datetime.today()
        print(f"Executing SQL Query: {query} on {date}")
        return func(*args, **kwargs)
    return wrapper

def create_table(query):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    
def insert_data(self):
    conn = self.connect_to_db()
    cursor = conn.cursor()
    sql = "INSERT INTO user (name, email, age) VALUES (?, ?, ?)"
    val = [
        ("Lekan", "lekan@gmail.com", 48),
        ("Oyesunle", "oyesunle@yahoo.com", 50)
    ]
    cursor.executemany(sql, val)
    conn.commit()
    cursor.close()

@log_queries    
def fetch_all_users(query):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

users = fetch_all_users(query="SELECT * FROM user;")

# connect_to_db()
# create_table(query="CREATE TABLE IF NOT EXISTS user (user_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, age INTEGER)")
# insert_data()
    