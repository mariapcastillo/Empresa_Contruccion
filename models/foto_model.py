from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FotoCreate(BaseModel):
    url: str = Field(..., min_length=5, max_length=500)
    descripcion: Optional[str] = None


class FotoResponse(BaseModel):
    id: int
    obra_id: int
    url: str
    descripcion: Optional[str] = None
    subido_por_user_id: int
    created_at: datetime

    class Config:
        from_attributes = True