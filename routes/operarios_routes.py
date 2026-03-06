from fastapi import APIRouter, Depends
from controllers import operarios_controller
from models.operario_model import OperarioCreate, OperarioUpdate
from core.dependences import require_admin

router = APIRouter(
    dependencies=[Depends(require_admin)]
)

@router.get("/", status_code=200)
async def get_all_operarios():
    return await operarios_controller.get_all_operarios()

@router.get("/{operario_id}", status_code=200)
async def get_operario_by_id(operario_id: int):
    return await operarios_controller.get_operario_by_id(operario_id)

@router.post("/", status_code=201)
async def create_operario(data: OperarioCreate):
    return await operarios_controller.create_operario(data)

@router.put("/{operario_id}", status_code=200)
async def update_operario(operario_id: int, data: OperarioUpdate):
    return await operarios_controller.update_operario(operario_id, data)

@router.delete("/{operario_id}", status_code=200)
async def delete_operario(operario_id: int):
    return await operarios_controller.delete_operario(operario_id)