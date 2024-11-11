from pydantic import BaseModel
from typing import Optional
from models.Mascotas_Extraviadas import Gender, Species

class MascotasExtraviadaRequest(BaseModel):
    nombre: str
    raza: str
    edad: int
    sexo: Gender
    especie: Species
    telefono: str
    direccion: str
    usuario: int
    imagen: Optional[str] = None
    fecha_extravio: str
    fecha_publicacion: str
    descripcion: str

class MascotasExtraviadasResponse(BaseModel):
    id: int
    nombre: str
    raza: str
    edad: int
    sexo: Gender
    especie: Species
    fecha_extravio: str
    fecha_publicacion: str
    descripcion: str
    imagen: Optional[str] = None
