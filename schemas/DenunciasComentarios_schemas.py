from pydantic import BaseModel

class DenunciasComentariosRequest(BaseModel):
    id_denuncia:int
    id_user:int
    comentario:str
    fecha:str

class DenunciasComentariosResponse(BaseModel):
    id:int
    id_denuncia:int
    id_user:int
    comentario:str
    fecha:str



   