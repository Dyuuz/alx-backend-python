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

def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result:
                args[0].commit()
                print("Success")
            else:
                raise Exception
        except Exception:
            args[0].rollback() 
            print("Error")
        return result
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor()
    cursor.execute(f"SELECT user_id FROM user WHERE user_id={user_id}")
    result = cursor.fetchone()
    if not result: 
        pass
    else:
        cursor.execute("UPDATE user SET email = ? WHERE user_id = ?", (new_email, user_id))
    return result

#### Update user's email with automatic transaction handling 
update_user_email(user_id=5, new_email='mary@hotmail.com'.lower()) 