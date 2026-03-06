from fastapi import HTTPException
import aiomysql as aio
from db.database import get_conn
from core.security import hash_password, verify_password, create_access_token


async def register_user(data):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            await cursor.execute(
                "SELECT id FROM users WHERE email = %s",
                (data.email,)
            )
            existing = await cursor.fetchone()

            if existing:
                raise HTTPException(status_code=400, detail="El email ya está registrado")

            hashed_password = hash_password(data.password)

            await cursor.execute("""
                INSERT INTO users (email, password, first_name, last_name, rol, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (
                data.email,
                hashed_password,
                data.first_name,
                data.last_name,
                data.rol
            ))

            await conn.commit()

            return {"message": "Usuario creado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


async def login_user(data):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            await cursor.execute("""
                SELECT id, email, password, rol
                FROM users
                WHERE email = %s
            """, (data.email,))
            user = await cursor.fetchone()

            if not user:
                raise HTTPException(status_code=401, detail="Credenciales inválidas")

            if not verify_password(data.password, user["password"]):
                raise HTTPException(status_code=401, detail="Credenciales inválidas")

            token = create_access_token({
                "sub": str(user["id"]),
                "rol": user["rol"]
            })

            return {
                "access_token": token,
                "token_type": "bearer"
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()