from fastapi import APIRouter, Depends
from controllers import notificacion_controller
from models.notificacion_model import NotificacionCreate, NotificacionResponse, NotificacionUpdate
from core.dependences import require_operario, get_current_user

router = APIRouter(
    dependencies=[Depends(require_operario)]
)

@router.post("/notificaciones", response_model=NotificacionResponse, status_code=201)
async def crear_notificacion(data: NotificacionCreate, current_user=Depends(get_current_user)):
    return await notificacion_controller.create_notificacion(current_user["id"], data)

@router.get("/notificaciones/{id}", response_model=NotificacionResponse, status_code=200)
async def get_notificacion(id: int, current_user=Depends(get_current_user)):
    return await notificacion_controller.get_notificacion_by_id_operario(id, current_user["id"])

@router.get("/notificaciones", response_model=list[NotificacionResponse], status_code=200)
async def get_all_notificaciones(
    tipo: str | None = None,
    obra_id: int | None = None,
    current_user=Depends(get_current_user)
):
    return await notificacion_controller.get_notificaciones_operario(current_user["id"], tipo, obra_id)

@router.put("/notificaciones/{notificacion_id}", response_model=NotificacionResponse, status_code=200)
async def upd_notificacion(
    notificacion_id: int,
    data: NotificacionUpdate,
    current_user=Depends(get_current_user)
):
    return await notificacion_controller.update_notificacion(notificacion_id, current_user["id"], data.mensaje)
