from sqlalchemy import Column, Integer, String, Enum, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
import enum
from db.database import Base

class RolEnum(str, enum.Enum):
    usuario = 'usuario'
    entidad = 'entidad'

class NombreCompletoType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value and isinstance(value, NombreCompleto):
            return f"({value.name},{value.last_name})"  
        return None

    def process_result_value(self, value, dialect):
        if value:
            value = value.strip(' ()')  
            parts = value.split(',')

            if len(parts) == 2:
                name, last_name = parts
                return NombreCompleto(name.strip(), last_name.strip())
            else:
                raise ValueError(f"Formato inválido para NombreCompleto: {value}")
        return None


class NombreCompleto:
    def __init__(self, name: str, last_name: str):
        self.name = name
        self.last_name = last_name

    def __str__(self):
        return f"{self.name} {self.last_name}"

class UserDB(Base):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(NombreCompletoType, nullable=False)  
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    rol = Column(Enum(RolEnum), nullable=False)

    def __init__(self, email, password, rol, name):
        if isinstance(name, NombreCompleto):
            self.name = name 
        else:
            raise ValueError("name must be an instance of NombreCompleto")
        self.email = email
        self.password = password
        self.rol = rol
