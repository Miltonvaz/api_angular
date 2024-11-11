from pydantic import BaseModel
from typing import List
from models.Entidad import TypeEntityEnum


class EntidadRequest(BaseModel):
    name: str
    address: str
    description: str
    type: TypeEntityEnum
    cellphone: str
    image: List[str]  
    id_user: int
    social_networks: List[str]

class EntidadResponse(BaseModel):
    id_entity: int
    name: str
    address: str
    description: str
    type: TypeEntityEnum
    cellphone: str
    image: List[str] 
    id_user: int
    social_networks: List[str]

    class Config:
        from_attributes = True
