import functools
import sqlite3
import time

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("user.db")
        try:
            args = (conn, *args) # Prepend connection, so other args will not be lost
            return func(*args, **kwargs)
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs): 
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"Attempts {attempts} failed: {e}")
                    if attempts < retries:
                        time.sleep(delay)
                    else:
                        print("All retry attempts failed")
                        raise
        return wrapper
    return decorator
                
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    result = cursor.fetchall()
    if not result:
        print("No result")
    else:
        print("Result")
    print(result)
    return result

#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()