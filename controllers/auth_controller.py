from fastapi import HTTPException
import aiomysql as aio
from db.database import get_conn
from core.security import hash_password, verify_password, create_access_token


async def register_user(data):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            # 1) comprobar si ya existe el email
            await cursor.execute("SELECT id FROM users WHERE email = %s", (data.email,))
            existing = await cursor.fetchone()
            if existing:
                raise HTTPException(status_code=400, detail="El email ya está registrado")

            # 2) hashear password
            password_hash = hash_password(data.password)

            # 3) insertar usuario
            await cursor.execute("""
                INSERT INTO users (email, password_hash, first_name, last_name, rol, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (data.email, password_hash, data.first_name, data.last_name, data.rol))

            await conn.commit()

            return {"message": "Usuario creado correctamente"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


async def login_user(data):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            # 1) buscar usuario por email
            await cursor.execute("""
                SELECT id, email, password_hash, rol
                FROM users
                WHERE email = %s
            """, (data.email,))
            user = await cursor.fetchone()

            if not user:
                raise HTTPException(status_code=401, detail="Credenciales inválidas")

            # 2) verificar password
            if not verify_password(data.password, user["password_hash"]):
                raise HTTPException(status_code=401, detail="Credenciales inválidas")

            # 3) crear token JWT
            token = create_access_token({
                "sub": str(user["id"]),
                "rol": user["rol"]
            })

            return {"access_token": token, "token_type": "bearer"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()