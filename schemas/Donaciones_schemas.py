from pydantic import BaseModel

class DonacionesRequest(BaseModel):
    user_id:int
    entidad_id:int
    cantidad:str
    fecha:str
    comprobante:str
    

class DonacionesResponse(BaseModel):
    id_donacion:int
    user_id:int
    entidad_id:int
    cantidad:str
    fecha:str
    comprobante:str
                        