from pydantic import BaseModel
from typing import Optional, Literal

Rol = Literal["admin", "operario"]


class OperarioProfile(BaseModel):
    operario_id: int
    especialidad: str
    estado: str
    localizacion: str
    telefono: str


class MeResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    rol: Rol
    foto_url: Optional[str] = None
    operario: Optional[OperarioProfile] = None