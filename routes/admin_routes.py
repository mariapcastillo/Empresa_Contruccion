from fastapi import APIRouter, HTTPException
from models.obra_model import ObraCreate, ObraUpdate, AsignarOperario
from controllers import admin_controller


router = APIRouter()


##Obtener todas las obras
@router.get("/obras", status_code=200)
async def get_all_obras():
    return await admin_controller.get_all_obras()

##Obtener una obra por su ID
@router.get("/obras/{id}", status_code=200)
async def get_obra_by_id(id: int):
    return await admin_controller.get_obra_by_id(id)

#Crear una nueva obra
@router.post("/obras", status_code=201)
async def create_obra(obra:ObraCreate):
    return await admin_controller.create_obra(obra)

##Actualizar una obra 
@router.put("/obras/{id}", status_code=200)
async def update_obra(id: int, obra:ObraUpdate):
    return await admin_controller.update_obra(id, obra)

##Eliminar una obra por su ID
@router.delete("/obras/{id}", status_code=200)
async def delete_obra(id: int):
    return await admin_controller.delete_obra(id)


##Para asignar un operario a la obra
@router.patch("/obras/{id}/asignar")
async def asignar_operario(id: int, data: AsignarOperario):
    return await admin_controller.asignar_operario(id, data.operario_id)