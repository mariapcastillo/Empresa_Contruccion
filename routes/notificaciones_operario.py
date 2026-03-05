from fastapi import APIRouter, Depends
from controllers import notificacion_controller
from schemas.notificacion_schema import NotificacionCreate, NotificacionResponse, NotificacionUpdate

router = APIRouter()


@router.post("/notificaciones", response_model=NotificacionResponse, status_code=201)
async def crear_notificacion(user_id: int, data: NotificacionCreate):
    return await notificacion_controller.create_notificacion(user_id, data)

@router.get("/notificaciones/{id}", response_model=NotificacionResponse, status_code=200)
async def get_notificacion(id: int, user_id: int):
    return await notificacion_controller.get_notificacion_by_id_operario(id, user_id)

@router.get("/notificaciones", response_model=list[NotificacionResponse], status_code=200)
async def get_all_notificaciones(user_id: int, tipo: str = None, obra_id: int = None):
    return await notificacion_controller.get_notificaciones_operario(user_id, tipo, obra_id)

@router.put("/notificaciones/{notificacion_id}", status_code=200)
async def upd_notificacion(notificacion_id: int, user_id: int, data: NotificacionUpdate):
    return await notificacion_controller.update_notificacion(notificacion_id, user_id, data.mensaje)

