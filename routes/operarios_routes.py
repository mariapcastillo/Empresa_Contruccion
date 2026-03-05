from fastapi import APIRouter, Depends
from controllers import operarios_controller
from models.operario_model import OperarioCreate, OperarioUpdate
from core.dependences import require_operario

router = APIRouter(
    dependencies=[Depends(require_operario)]
)

@router.get("/", status_code=200)
async def get_all_operarios():
    return await operarios_controller.get_all_operarios()

@router.get("/{id}", status_code=200)
async def get_operario_by_id(id: int):
    return await operarios_controller.get_operario_by_id(id)

@router.post("/", status_code=201)
async def create_operario(operario: OperarioCreate):
    return await operarios_controller.create_operario(operario)

@router.put("/{id}", status_code=200)
async def update_operario(id: int, operario: OperarioUpdate):
    return await operarios_controller.update_operario(id, operario)

@router.delete("/{id}", status_code=200)
async def delete_operario(id: int):
    return await operarios_controller.delete_operario(id)