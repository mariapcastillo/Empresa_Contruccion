from db.database import get_conn
import aiomysql as aio
from fastapi import HTTPException

# ── OPERARIO ──────────────────────────────────────────

async def get_notificaciones_operario(user_id: int, tipo=None, obra_id=None):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            conditions = ["user_id = %s"]  # siempre obligatorio
            values = [user_id]

            if tipo:
                conditions.append("tipo = %s")
                values.append(tipo)

            if obra_id:
                conditions.append("obra_id = %s")
                values.append(obra_id)

            where = " AND ".join(conditions)

            await cursor.execute(f"""
                SELECT * FROM notificaciones
                WHERE {where}
                ORDER BY created_at DESC
            """, values)

            return await cursor.fetchall()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

async def create_notificacion(user_id: int, data):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            await cursor.execute("""
                INSERT INTO notificaciones (user_id, obra_id, tipo, mensaje)
                VALUES (%s, %s, %s, %s)
            """, (
                user_id,
                data.obra_id,
                data.tipo, 
                data.mensaje
            ))                         

            await conn.commit()                    # 1. guarda el INSERT
            new_id = cursor.lastrowid             # 2. captura el id generado
                                                # 3. busca el registro recién creado
            await cursor.execute("""              
                SELECT * FROM notificaciones WHERE id = %s
                """, (new_id,))

            return await cursor.fetchone()        # 4. devuelve el objeto completo

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

async def get_notificacion_by_id_operario(id: int, user_id: int):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            await cursor.execute("""
            SELECT * FROM notificaciones WHERE id = %s
            """, (id,))

            notificacion = await cursor.fetchone()

            # caso 1: no existe
            if not notificacion:
                raise HTTPException(status_code=404, detail="Notificacion no encontrada")

            # caso 2: existe pero no es tuya
            if notificacion["user_id"] != user_id:
                raise HTTPException(status_code=403, detail="No tienes los permisos necesarios")

            # caso 3: todo ok
            return notificacion
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

async def update_notificacion(notificacion_id: int, user_id: int, mensaje: str):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

                await cursor.execute("""
                SELECT * FROM notificaciones WHERE id = %s
                """, (notificacion_id,))

                notificacion = await cursor.fetchone()

                # caso 1: no existe
                if not notificacion:
                    raise HTTPException(status_code=404, detail="Notificacion no encontrada")

                # caso 2: existe pero no es tuya
                if notificacion["user_id"] != user_id:
                        raise HTTPException(status_code=403, detail="No tienes los permisos necesarios")

                # caso 3: todo ok
                await cursor.execute("""
                    UPDATE notificaciones SET mensaje = %s WHERE id = %s
                """, (mensaje, notificacion_id))

                await conn.commit()
                
                await cursor.execute("""              
                SELECT * FROM notificaciones WHERE id = %s
                """, (notificacion_id,))

                return await cursor.fetchone()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

# ── ADMIN ─────────────────────────────────────────────

async def get_all_notificaciones(tipo=None, obra_id=None, is_read=None):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            conditions = [] 
            values = []

            if tipo:
                conditions.append("tipo = %s")
                values.append(tipo)

            if obra_id:
                conditions.append("obra_id = %s")
                values.append(obra_id)

            if is_read is not None:
                conditions.append("is_read = %s")
                values.append(is_read)

            where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

            await cursor.execute(f"""
                SELECT * FROM notificaciones
                {where}
                ORDER BY created_at DESC
            """, values)

            return await cursor.fetchall()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


async def cerrar_notificacion(notificacion_id: int):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

            await cursor.execute("""
                SELECT * FROM notificaciones WHERE id = %s
            """, (notificacion_id,))

            notificacion = await cursor.fetchone()

            if not notificacion:
                raise HTTPException(status_code=404, detail="Notificacion no encontrada")

            if notificacion["tipo"] != "incidencia":
                raise HTTPException(status_code=400, detail="Solo se pueden cerrar notificaciones de tipo incidencia")

            await cursor.execute("""
                UPDATE notificaciones SET is_read = %s WHERE id = %s
            """, (1, notificacion_id))

            await conn.commit()
            return {"message": "Notificacion cerrada"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

async def delete_notificacion(notificacion_id: int):
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

                await cursor.execute("""
                SELECT * FROM notificaciones WHERE id = %s
                """, (notificacion_id,))

                notificacion = await cursor.fetchone()

                # caso 1: no existe
                if not notificacion:
                    raise HTTPException(status_code=404, detail="Notificacion no encontrada")
         
                # caso 2: delete
                await cursor.execute("""
                DELETE FROM notificaciones WHERE id = %s
                """, (notificacion_id,))

                await conn.commit()
                return {"message": "Notificacion eliminada"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

# -- SIRVE PARA AMBOS:
async def get_notificacion_by_id(notificacion_id: int, user_id: int,rol: str):
    # Tarea: SELECT simple por id, solo 404 si no existe
    conn = None
    try:
        conn = await get_conn()
        async with conn.cursor(aio.DictCursor) as cursor:

                await cursor.execute("""
                SELECT * FROM notificaciones WHERE id = %s
                """, (notificacion_id,))

                notificacion = await cursor.fetchone()

                # caso 1: no existe
                if not notificacion:
                    raise HTTPException(status_code=404, detail="Notificacion no encontrada")

                # caso 2: existe pero no es tuya
                if rol == 'operario':
                    if notificacion["user_id"] != user_id:
                        raise HTTPException(status_code=403, detail="No tienes los permisos necesarios")

                # caso 3: todo ok
                return notificacion
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()