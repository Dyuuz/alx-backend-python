from django.db import connection
import functools, uuid

def generate_uuid():
    id = uuid.uuid4()
    print(str(id))
    return str(id)

def database_wrapper(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        args = (conn, *args)
        with connection.cursor() as cursor:
            conn = cursor
            result = func(*args, **kwargs)
            print(f"Executed query: {func.__name__} with args: {args}, kwargs: {kwargs}")
        return result
    return wrapper

@database_wrapper
def insert_into_user_table(conn, fn, ln, email, phone_number, password): 
    user_id = generate_uuid()
    query = '''
            INSERT INTO chats_user (user_id, first_name, last_name, email, phone_number, password)
            VALUES (%s, %s, %s, %s, %s, %s);
            '''
    conn.execute(query, (user_id, fn, ln, email, phone_number, password))
    return conn.fetchone()

@database_wrapper
def select_all_from_user_table(conn):
    query = '''
            SELECT * FROM chats_user;
        '''
    conn.execute(query)
    return conn.fetchall()