from fastapi import APIRouter, Depends
from controllers import notificacion_controller
from schemas.notificacion_schema import NotificacionCreate, NotificacionResponse

router = APIRouter()


@router.post("/notificaciones", response_model=NotificacionResponse, status_code=201)
async def crear_notificacion(user_id: int, data: NotificacionCreate):
    return await notificacion_controller.create_notificacion(user_id, data)

@router.get("/notificaciones/{id}", response_model=NotificacionResponse, status_code=200)
async def get_notificacion(id: int, user_id: int):
    return await notificacion_controller.get_notificacion_by_id_operario(id, user_id)