import asyncio
import aiomysql

async def test_db():
    try:
        connection = await aiomysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="12345678",
            db="empresa_construccion"
        )

        async with connection.cursor() as cursor:
            await cursor.execute("SELECT 1;")
            result = await cursor.fetchone()
            print("✅ Conexión exitosa:", result)

        connection.close()

    except Exception as e:
        print("❌ Error de conexión:", e)

asyncio.run(test_db())