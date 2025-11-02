from dotenv import load_dotenv
import mysql.connector, os, pandas, uuid
load_dotenv(override=True)

def connect_db():
    connect_to_db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = os.environ.get("PASSWORD")
    )
    return connect_to_db


def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()
    print("Database created")

def connect_to_prodev():
    db = connect_db()
    db.connect(database="ALX_prodev")

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("USE ALX_prodev")
    cursor.execute("CREATE TABLE IF NOT EXISTS user_data (user_id CHAR(36) Primary Key, name VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, age DECIMAL(3, 0)NOT NULL)")
    cursor.execute("SHOW TABLES;")
    print(cursor.fetchall())
    cursor.close()
    print("Table created")

def insert_data(connection, data):
    read = pandas.read_csv(data)
    data = read.to_dict()
    name, email, age = data['name'], data['email'], data['age']
    cursor = connection.cursor()
    cursor.execute("USE ALX_prodev")
    user_id = str(uuid.uuid4())
    val = []
    for v in range(len(name)):
        user_id = str(uuid.uuid4())
        user_info = (user_id, name[v], email[v], age[v])
        val.append(user_info,)
    sql = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
    cursor.executemany(sql, val)
    connection.commit()
    print("Data Inserted")
    cursor.close()

# create_table(connect_db())
# insert_data(connection=connect_db(), data="user_data.csv")

 