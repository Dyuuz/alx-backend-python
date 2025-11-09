import functools
import sqlite3

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

query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')
        if query in query_cache:
            return query_cache[query]
        
        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"Caching result for query: {query}")
        print(query_cache)
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM user")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT name FROM user WHERE user_id=1")