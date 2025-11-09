import aiosqlite, asyncio

db_file_path = "user.db"

async def async_fetch_users():
    async with aiosqlite.connect(database=db_file_path) as db:
        async with db.execute("SELECT * FROM user") as cursor:
               return await cursor.fetchall()

async def async_fetch_older_users():
    async with aiosqlite.connect(database=db_file_path) as db:
        async with db.execute("SELECT * FROM user WHERE age > 40") as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    return await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
        )

users, older_users = asyncio.run(fetch_concurrently())
print(f"All users: ", users)
print("Older users: ", older_users)