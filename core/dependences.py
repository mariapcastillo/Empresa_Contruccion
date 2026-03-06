from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import aiomysql as aio

from db.database import get_conn
from core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido (sub missing)")

    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                SELECT id, email, first_name, last_name, rol
                FROM users
                WHERE id = %s
            """, (user_id,))
            user = await cursor.fetchone()

            if not user:
                raise HTTPException(status_code=401, detail="Usuario no encontrado")

            return user

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


async def require_admin(current_user=Depends(get_current_user)):
    if current_user["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado: solo admin")
    return current_user


async def require_operario(current_user=Depends(get_current_user)):
    if current_user["rol"] != "operario":
        raise HTTPException(status_code=403, detail="Acceso denegado: solo operario")
    return current_user