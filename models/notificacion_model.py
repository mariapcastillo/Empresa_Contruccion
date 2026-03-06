from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class TipoNotificacion(str, Enum):
    incidencia = "incidencia"
    avance = "avance"
    material = "material"


class NotificacionCreate(BaseModel):
    obra_id: int
    tipo: TipoNotificacion
    mensaje: str


class NotificacionUpdate(BaseModel):
    mensaje: str


class NotificacionResponse(BaseModel):
    id: int
    user_id: int
    obra_id: int
    tipo: TipoNotificacion
    mensaje: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True