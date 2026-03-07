from fastapi import APIRouter, Depends
from core.dependences import require_operario
from controllers import obras_controller

router = APIRouter(
    dependencies=[Depends(require_operario)]
)

# Obtener todas las obras asignadas al operario logueado
@router.get("/obras", status_code=200)
async def get_mis_obras(current_user=Depends(require_operario)):
    return await obras_controller.get_obras_operario(current_user["id"])


# Obtener una obra concreta del operario
@router.get("/obras/{obra_id}", status_code=200)
async def get_mi_obra(obra_id: int, current_user=Depends(require_operario)):
    return await obras_controller.get_obra_operario_by_id(
        obra_id,
        current_user["id"]
    )