from fastapi import HTTPException
from models.operario_model import OperarioCreate, OperarioUpdate
import aiomysql as aio
from db.database import get_conn 


async def get_all_operarios():
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                SELECT id, user_id, especialidad, estado, localizacion, telefono
                FROM operarios
                ORDER BY id DESC
            """)
            rows = await cursor.fetchall()
            return rows

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


async def get_operario_by_id(operario_id: int):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                SELECT id, user_id, especialidad, estado, localizacion, telefono
                FROM operarios
                WHERE id = %s
            """, (operario_id,))
            row = await cursor.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="Operario no encontrado")

            return row

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


async def create_operario(operario: OperarioCreate):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            # 1) Validar user existe
            await cursor.execute("SELECT id, rol FROM users WHERE id = %s", (operario.user_id,))
            user_row = await cursor.fetchone()
            if not user_row:
                raise HTTPException(status_code=400, detail="user_id no existe")

            # 2) Validar rol = operario
            if user_row["rol"] != "operario":
                raise HTTPException(status_code=400, detail="El usuario no tiene rol 'operario'")

            # 3) Insert
            try:
                await cursor.execute("""
                    INSERT INTO operarios (user_id, especialidad, estado, localizacion, telefono)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    operario.user_id,
                    operario.especialidad,
                    operario.estado,
                    operario.localizacion,
                    operario.telefono
                ))
                await conn.commit()
            except Exception as e:
                await conn.rollback()
                # Caso típico: user_id duplicado por UNIQUE uq_operarios_user
                raise HTTPException(status_code=409, detail=f"No se pudo crear operario: {str(e)}")

            new_id = cursor.lastrowid

            # 4) devolver creado
            await cursor.execute("""
                SELECT id, user_id, especialidad, estado, localizacion, telefono
                FROM operarios
                WHERE id = %s
            """, (new_id,))
            created = await cursor.fetchone()
            return created

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


async def update_operario(operario_id: int, operario: OperarioUpdate):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            await cursor.execute("""
                UPDATE operarios
                SET especialidad = %s,
                    estado = %s,
                    localizacion = %s,
                    telefono = %s
                WHERE id = %s
            """, (
                operario.especialidad,
                operario.estado,
                operario.localizacion,
                operario.telefono,
                operario_id
            ))

            await conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Operario no encontrado")

            return {"message": "Operario actualizado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


async def delete_operario(operario_id: int):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            # verificar existe
            await cursor.execute("SELECT * FROM operarios WHERE id = %s", (operario_id,))
            exists = await cursor.fetchone()
            if not exists:
                raise HTTPException(status_code=404, detail="Operario no encontrado")

            await cursor.execute("DELETE FROM operarios WHERE id = %s", (operario_id,))
            await conn.commit()

            return {"message": "Operario eliminado", "id": operario_id}

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()