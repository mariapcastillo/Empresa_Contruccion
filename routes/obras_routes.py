from fastapi import APIRouter, Depends
from models.obras_model import ObraCreate, ObraUpdate, AsignarOperario
from controllers import obras_controller
from core.dependences import require_admin

router = APIRouter(
    dependencies=[Depends(require_admin)]
)


##Obtener todas las obras
@router.get("/", status_code=200)
async def get_all_obras():
    return await obras_controller.get_all_obras()

##Obtener una obra por su ID
@router.get("/{id}", status_code=200)
async def get_obra_by_id(id: int):
    return await obras_controller.get_obra_by_id(id)

#Crear una nueva obra
@router.post("/", status_code=201)
async def create_obra(obra:ObraCreate):
    return await obras_controller.create_obra(obra)

##Actualizar una obra 
@router.put("/{id}", status_code=200)
async def update_obra(id: int, obra:ObraUpdate):
    return await obras_controller.update_obra(id, obra)

##Eliminar una obra por su ID
@router.delete("/{id}", status_code=200)
async def delete_obra(id: int):
    return await obras_controller.delete_obra(id)


##Para asignar un operario a la obra
@router.patch("/{id}/asignar")
async def asignar_operario(id: int, data: AsignarOperario):
    return await obras_controller.asignar_operario(id, data.operario_id)