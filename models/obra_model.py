from pydantic import BaseModel, Field
from typing import Optional, Literal

EstadoObra = Literal["pendiente", "en_progreso", "completada"]


class ObraCreate(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=200)
    descripcion: str = Field(..., min_length=2)
    categoria: str = Field(..., min_length=2, max_length=100)
    localizacion: str = Field(..., min_length=2, max_length=200)


class ObraUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=2, max_length=200)
    descripcion: Optional[str] = Field(None, min_length=2)
    categoria: Optional[str] = Field(None, min_length=2, max_length=100)
    localizacion: Optional[str] = Field(None, min_length=2, max_length=200)
    estado: Optional[EstadoObra] = None


class AsignarOperario(BaseModel):
    operario_id: int = Field(..., gt=0, description="ID del operario que se asignará a la obra")
