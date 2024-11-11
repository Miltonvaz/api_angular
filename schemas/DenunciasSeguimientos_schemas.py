from pydantic import BaseModel

class DenunciaSeguimientoRequest(BaseModel):
    id_entidad:int
    fecha:str
    descripcion:str


class DenunciaSeguimientoResponse(BaseModel):
    id_entidad:int
    fecha:str
    descripcion:str



