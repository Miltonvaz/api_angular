from pydantic import BaseModel
from enum import Enum as PythonEnum

from models.Mascotas import Gender, Size, Species

class MascotasRequest(BaseModel):
    name: str
    age: int
    race: str
    weight: float
    gender: Gender
    species: Species
    size: Size
    image: str
    entity_id: int

class MascotasResponse(BaseModel):
    id_mascota: int
    name: str
    age: int
    race: str
    weight: float
    gender: Gender
    species: Species
    size: Size
    image: str
    entity_id: int
