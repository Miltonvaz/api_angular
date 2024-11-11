from sqlalchemy import String, Integer, Column, ForeignKey, Enum as SqlEnum, ARRAY
from sqlalchemy.orm import relationship
from db.database import Base
from enum import Enum
import sys


class TypeEntityEnum(str, Enum):
    refugio = "refugio"
    veterinaria = "veterinaria"
    perrera = "perrera"
    centros_de_adopcion = "centros de adopción"

class EntidadDB(Base):
    __tablename__ = "entity"
    
    id_entity = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(150), nullable=False)
    type = Column(SqlEnum(TypeEntityEnum), nullable=False)  
    cellphone = Column(String(15))
    image = Column(String(255))
    description = Column(String)
    id_user = Column(Integer, ForeignKey('users.id_user'), unique=True, nullable=True) 
    social_networks = Column(ARRAY(String), nullable=False)  
    
    