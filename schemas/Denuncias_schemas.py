from pydantic import BaseModel
from typing import List

class DenunciasRequest(BaseModel):
    id_usuario: int
    motivo: str
    id_institucion: int
    descripcion: str
    imagen: List[str] 
    id_mascota: int

class DenunciasResponse(BaseModel):
    id_denuncia: int
    id_user: int
    motivo: str
    id_institucion: int
    descripcion: str
    imagen: str  
    id_mascota: int

    class Config:
        from_attributes = True
