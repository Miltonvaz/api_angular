from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class RolEnum(str, Enum):
    admin = "usuario"
    user = "entidad"



class NombreCompleto(BaseModel):
    name: str
    last_name: str

    class Config:
        from_attributes = True  


class UserCreate(BaseModel):
    nombre_completo: NombreCompleto
    email: EmailStr
    password: str
    rol: RolEnum

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id_user: int
    nombre_completo:str
    email: EmailStr
    rol: RolEnum

    class Config:
        from_attributes = True  


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
 

# Model for login response
class LoginResponse(BaseModel):
    id_user: int
    name: str
    lastName: str
    email: EmailStr
    rol: RolEnum
    access_token: str



class UpdateUserRequest(BaseModel):
    name: str
    lastName: str
    email: EmailStr
    password: Optional[str]
    rol: RolEnum


class EntidadRegistrationResponse(BaseModel):
    message: str
    user_id: int
