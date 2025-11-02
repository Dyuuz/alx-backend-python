from seed import connect_db

def paginate_users(page_size:int, offset: int = 0):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("USE ALX_prodev")
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    paginated = cursor.fetchall()
    data = [{ "user_id": row[0], "name": row[1], "email": row[2], "age": int(row[3])} for row in paginated]
    cursor.close()
    return data

def lazy_paginate(page_size:int):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

    
try:
    for page in lazy_paginate(5):
        for user in page:
            print(user)
except Exception as e:
    print(e)