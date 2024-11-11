from pydantic import BaseModel
from typing import Optional
from models.Adopciones import StatusAdoption

class AdopcionRequest(BaseModel):
    id_mascota: int
    id_usuario: int
    fecha_adopcion: str
    curp: str
    imagen: str
    seguimiento: Optional[str]
    observaciones: str
    condiciones: str
    status: StatusAdoption  

class AdopcionResponse(BaseModel):
    id_mascota: int
    id_usuario: int
    fecha_adopcion: str
    curp: str
    imagen: str
    seguimiento: Optional[str]
    observaciones: str
    condiciones: str
    status: StatusAdoption
