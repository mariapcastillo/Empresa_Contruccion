import os
from dotenv import load_dotenv
import aiomysql

load_dotenv()

print("HOST:", os.getenv("MYSQL_HOST"))
print("USER:", os.getenv("MYSQL_USER"))

async def get_conn():
    return await aiomysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DATABASE"),
        autocommit=True,
    )

async def test_db_connection():
    conn = await get_conn()
    try:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 1")
            await cur.fetchone()
    finally:
        conn.close()