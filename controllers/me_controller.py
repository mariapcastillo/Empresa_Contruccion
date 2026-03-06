from fastapi import HTTPException
import aiomysql as aio
from db.database import get_conn


async def get_me(user_id: int):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            await cursor.execute("""
                SELECT 
                    u.id,
                    u.email,
                    u.first_name,
                    u.last_name,
                    u.rol,
                    u.foto_url,
                    o.id AS operario_id,
                    o.especialidad,
                    o.estado,
                    o.localizacion,
                    o.telefono
                FROM users u
                LEFT JOIN operarios o ON u.id = o.user_id
                WHERE u.id = %s
            """, (user_id,))

            row = await cursor.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            response = {
                "id": row["id"],
                "email": row["email"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "rol": row["rol"],
                "foto_url": row["foto_url"],
                "operario": None
            }

            if row["rol"] == "operario" and row["operario_id"]:
                response["operario"] = {
                    "operario_id": row["operario_id"],
                    "especialidad": row["especialidad"],
                    "estado": row["estado"],
                    "localizacion": row["localizacion"],
                    "telefono": row["telefono"]
                }

            return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()