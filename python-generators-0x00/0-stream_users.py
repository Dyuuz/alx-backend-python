from seed import connect_db

def stream_users():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("USE ALX_prodev")
    cursor.execute("SELECT user_id, name, email, age FROM user_data")
    for row in cursor:
        yield {
            "user_id": row[0],
            "name": row[1],
            "email": row[2],
            "age": int(row[3])
        }
    cursor.close()
    connection.close()