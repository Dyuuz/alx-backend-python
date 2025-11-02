from seed import connect_db

def stream_user_ages():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("USE ALX_prodev")
    cursor.execute(f"SELECT age FROM user_data")
    for row in cursor:
        yield int(row[0])

def average_age():
    total = 0
    count = 1
    for age in stream_user_ages():
        total += age
        count += 1
    if count == 0:
        print("No users found.")
    else:
        avg = total / count
        print("Average age of users: ", round(avg, 2))

average_age()