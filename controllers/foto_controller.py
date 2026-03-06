from fastapi import HTTPException
import aiomysql as aio
from db.database import get_conn


# ---------------- ADMIN ----------------

async def get_fotos_admin(obra_id: int):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT id FROM obras WHERE id = %s", (obra_id,))
            obra = await cursor.fetchone()
            if not obra:
                raise HTTPException(status_code=404, detail="Obra no encontrada")

            await cursor.execute("""
                SELECT id, obra_id, url, descripcion, subido_por_user_id, created_at
                FROM fotos
                WHERE obra_id = %s
                ORDER BY created_at DESC
            """, (obra_id,))
            return await cursor.fetchall()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


async def create_foto_admin(obra_id: int, user_id: int, data):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT id FROM obras WHERE id = %s", (obra_id,))
            obra = await cursor.fetchone()
            if not obra:
                raise HTTPException(status_code=404, detail="Obra no encontrada")

            await cursor.execute("""
                INSERT INTO fotos (obra_id, url, descripcion, subido_por_user_id)
                VALUES (%s, %s, %s, %s)
            """, (obra_id, data.url, data.descripcion, user_id))

            await conn.commit()
            foto_id = cursor.lastrowid

            await cursor.execute("""
                SELECT id, obra_id, url, descripcion, subido_por_user_id, created_at
                FROM fotos
                WHERE id = %s
            """, (foto_id,))
            return await cursor.fetchone()

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


async def delete_foto_admin(obra_id: int, foto_id: int):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                DELETE FROM fotos
                WHERE id = %s AND obra_id = %s
            """, (foto_id, obra_id))

            await conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Foto no encontrada")

            return {"message": "Foto eliminada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


# ---------------- OPERARIO ----------------

async def get_fotos_operario(obra_id: int, user_id: int):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            await cursor.execute("""
                SELECT o.id
                FROM obras o
                JOIN operarios op ON o.operario_id = op.id
                WHERE o.id = %s AND op.user_id = %s
            """, (obra_id, user_id))
            obra = await cursor.fetchone()

            if not obra:
                raise HTTPException(status_code=403, detail="No puedes ver fotos de esta obra")

            await cursor.execute("""
                SELECT id, obra_id, url, descripcion, subido_por_user_id, created_at
                FROM fotos
                WHERE obra_id = %s
                ORDER BY created_at DESC
            """, (obra_id,))
            return await cursor.fetchall()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


async def create_foto_operario(obra_id: int, user_id: int, data):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            await cursor.execute("""
                SELECT o.id
                FROM obras o
                JOIN operarios op ON o.operario_id = op.id
                WHERE o.id = %s AND op.user_id = %s
            """, (obra_id, user_id))
            obra = await cursor.fetchone()

            if not obra:
                raise HTTPException(status_code=403, detail="No puedes subir fotos a esta obra")

            await cursor.execute("""
                INSERT INTO fotos (obra_id, url, descripcion, subido_por_user_id)
                VALUES (%s, %s, %s, %s)
            """, (obra_id, data.url, data.descripcion, user_id))

            await conn.commit()
            foto_id = cursor.lastrowid

            await cursor.execute("""
                SELECT id, obra_id, url, descripcion, subido_por_user_id, created_at
                FROM fotos
                WHERE id = %s
            """, (foto_id,))
            return await cursor.fetchone()

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


async def delete_foto_operario(obra_id: int, foto_id: int, user_id: int):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            await cursor.execute("""
                DELETE f
                FROM fotos f
                JOIN obras o ON f.obra_id = o.id
                JOIN operarios op ON o.operario_id = op.id
                WHERE f.id = %s
                  AND f.obra_id = %s
                  AND op.user_id = %s
                  AND f.subido_por_user_id = %s
            """, (foto_id, obra_id, user_id, user_id))

            await conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Foto no encontrada o no autorizada")

            return {"message": "Foto eliminada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()