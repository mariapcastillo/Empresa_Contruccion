from fastapi import HTTPException
from models.obras_model import ObraCreate, ObraUpdate
import aiomysql as aio
from db.database import get_conn


# GET ALL OBRAS
async def get_all_obras():
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                SELECT id, titulo, descripcion, categoria, localizacion, operario_id, estado, foto
                FROM obras
                ORDER BY id DESC
            """)
            rows = await cursor.fetchall()
            return rows

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


# GET OBRA BY ID
async def get_obra_by_id(id: int):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                SELECT id, titulo, descripcion, categoria, localizacion, operario_id, estado, foto
                FROM obras
                WHERE id = %s
            """, (id,))
            row = await cursor.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="Obra no encontrada")

            return row

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


# CREATE OBRA
async def create_obra(obra: ObraCreate):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                INSERT INTO obras (titulo, descripcion, categoria, localizacion, estado, created_at, fecha_inicio, updated_at)
                VALUES (%s, %s, %s, %s, 'pendiente', NOW(), NOW(), NOW())
            """, (
                obra.titulo,
                obra.descripcion,
                obra.categoria,
                obra.localizacion
            ))

            await conn.commit()
            return {"message": "Obra creada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


# UPDATE OBRA
async def update_obra(id: int, obra: ObraUpdate):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                UPDATE obras
                SET titulo = %s,
                    descripcion = %s,
                    categoria = %s,
                    localizacion = %s,
                    estado = %s,
                    updated_at = NOW()
                WHERE id = %s
            """, (
                obra.titulo,
                obra.descripcion,
                obra.categoria,
                obra.localizacion,
                obra.estado,
                id
            ))

            await conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Obra no encontrada")

            return {"message": "Obra actualizada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


# DELETE OBRA
async def delete_obra(id: int):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                DELETE FROM obras
                WHERE id = %s
            """, (id,))

            await conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Obra no encontrada")

            return {"message": "Obra eliminada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


# ASIGNAR OPERARIO A OBRA
async def asignar_operario(obra_id: int, operario_id: int):
    conn = None
    try:
        conn = await get_conn()

        async with conn.cursor(aio.DictCursor) as cursor:

            # comprobar que la obra existe
            await cursor.execute("""
                SELECT id, estado, operario_id, categoria
                FROM obras
                WHERE id = %s
            """, (obra_id,))
            obra = await cursor.fetchone()

            if not obra:
                raise HTTPException(status_code=404, detail="Obra no encontrada")

            if obra["estado"] == "completada":
                raise HTTPException(status_code=400, detail="La obra ya está completada")

            # comprobar que el operario existe
            await cursor.execute("""
                SELECT id, estado, especialidad
                FROM operarios
                WHERE id = %s
            """, (operario_id,))
            operario = await cursor.fetchone()

            if not operario:
                raise HTTPException(status_code=404, detail="Operario no encontrado")

            # comprobar disponibilidad
            if operario["estado"] != "disponible":
                raise HTTPException(status_code=400, detail="El operario no está disponible")

            # comprobar si ya tiene obra activa
            await cursor.execute("""
                SELECT id
                FROM obras
                WHERE operario_id = %s
                AND estado IN ('pendiente', 'en progreso')
                LIMIT 1
            """, (operario_id,))
            asignacion = await cursor.fetchone()

            if asignacion:
                raise HTTPException(status_code=409, detail="El operario ya tiene una obra asignada")

            # asignar operario a la obra
            await cursor.execute("""
                UPDATE obras
                SET operario_id = %s,
                    estado = 'en progreso',
                    updated_at = NOW()
                WHERE id = %s
            """, (operario_id, obra_id))

            # cambiar estado del operario
            await cursor.execute("""
                UPDATE operarios
                SET estado = 'ocupado'
                WHERE id = %s
            """, (operario_id,))

            await conn.commit()

            return {
                "message": "Operario asignado correctamente",
                "obra_id": obra_id,
                "operario_id": operario_id
            }

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

async def get_obras_operario(user_id: int):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                SELECT 
                    o.id,
                    o.titulo,
                    o.descripcion,
                    o.categoria,
                    o.localizacion,
                    o.operario_id,
                    o.estado,
                    f.url AS foto
                FROM obras o
                JOIN operarios op ON o.operario_id = op.id
                LEFT JOIN fotos f ON f.obra_id = o.id
                WHERE op.user_id = %s
                GROUP BY o.id, o.titulo, o.descripcion, o.categoria, o.localizacion, o.operario_id, o.estado, f.url
                ORDER BY o.id DESC
            """, (user_id,))

            return await cursor.fetchall()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()