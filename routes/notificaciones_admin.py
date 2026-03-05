from fastapi import APIRouter, Depends
from controllers import notificacion_controller
from schemas.notificacion_schema import NotificacionCreate, NotificacionResponse, NotificacionUpdate


router = APIRouter()

@router.get("/notificaciones", response_model=list[NotificacionResponse], status_code=200)
async def get_all_notificaciones(tipo=None, obra_id=None, is_read=None):
    return await notificacion_controller.get_all_notificaciones(tipo, obra_id, is_read)

@router.get("/notificaciones/{id}", response_model=NotificacionResponse, status_code=200 )
async def get_notificacion_id(id: int, user_id: int,rol: str):
    return await notificacion_controller.get_notificacion_by_id(id,user_id, rol)

@router.patch("/notificaciones/{id}/cerrar", status_code=200)
async def cerrar_incidencia(id: int):
    return await notificacion_controller.cerrar_notificacion(id)

@router.delete("/notificaciones/{id}", status_code=204)
async def delete_notificacion(id: int):
    return await notificacion_controller.delete_notificacion(id)