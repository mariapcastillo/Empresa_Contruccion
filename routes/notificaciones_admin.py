from core.dependences import get_current_user
from fastapi import APIRouter, Depends
from controllers import notificacion_controller
from models.notificacion_model import NotificacionCreate, NotificacionResponse, NotificacionUpdate


router = APIRouter()

@router.get("/notificaciones", response_model=list[NotificacionResponse], status_code=200)
async def get_all_notificaciones(tipo: str | None = None, obra_id: int | None = None, is_read: bool | None = None):
    return await notificacion_controller.get_all_notificaciones(tipo, obra_id, is_read)

@router.get("/notificaciones/{id}", response_model=NotificacionResponse, status_code=200)
async def get_notificacion_id(id: int, current_user=Depends(get_current_user)):
    return await notificacion_controller.get_notificacion_by_id(id, current_user["id"], current_user["rol"])

@router.patch("/notificaciones/{id}/cerrar", status_code=200)
async def cerrar_incidencia(id: int):
    return await notificacion_controller.cerrar_notificacion(id)

@router.delete("/notificaciones/{id}", status_code=200)
async def delete_notificacion(id: int):
    return await notificacion_controller.delete_notificacion(id)