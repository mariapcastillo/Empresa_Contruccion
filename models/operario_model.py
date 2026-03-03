from pydantic import BaseModel, Field
from typing import Optional, Literal

EstadoOperario = Literal["disponible", "ocupado"]


class OperarioCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    especialidad: str = Field(..., min_length=2, max_length=100)
    estado: EstadoOperario
    localizacion: str = Field(..., min_length=2, max_length=255)
    telefono: str = Field(..., min_length=6, max_length=15)


class OperarioUpdate(BaseModel):
    especialidad: Optional[str] = Field(None, min_length=2, max_length=100)
    estado: Optional[EstadoOperario] = None
    localizacion: Optional[str] = Field(None, min_length=2, max_length=255)
    telefono: Optional[str] = Field(None, min_length=6, max_length=15)