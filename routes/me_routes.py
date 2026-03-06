from fastapi import APIRouter, Depends
from core.dependences import get_current_user
from controllers.me_controller import get_me
from models.me_model import MeResponse

router = APIRouter()

@router.get("/me", response_model=MeResponse, status_code=200)
async def read_me(current_user=Depends(get_current_user)):
    return await get_me(current_user["id"])

###FALTA RUTA PUT ME PARA MODIFICAR 