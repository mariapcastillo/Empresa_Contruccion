from fastapi import APIRouter, Depends
from core.dependences import require_operario, get_current_user
from controllers import foto_controller
from models.foto_model import FotoCreate, FotoResponse

router = APIRouter(
    dependencies=[Depends(require_operario)]
)

@router.get("/obras/{obra_id}/fotos", response_model=list[FotoResponse], status_code=200)
async def get_fotos(obra_id: int, current_user=Depends(get_current_user)):
    return await foto_controller.get_fotos_operario(obra_id, current_user["id"])

@router.post("/obras/{obra_id}/fotos", response_model=FotoResponse, status_code=201)
async def create_foto(obra_id: int, data: FotoCreate, current_user=Depends(get_current_user)):
    return await foto_controller.create_foto_operario(obra_id, current_user["id"], data)

@router.delete("/obras/{obra_id}/fotos/{foto_id}", status_code=200)
async def delete_foto(obra_id: int, foto_id: int, current_user=Depends(get_current_user)):
    return await foto_controller.delete_foto_operario(obra_id, foto_id, current_user["id"])