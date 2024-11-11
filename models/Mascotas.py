from sqlalchemy import String, Integer, Column, ForeignKey, Numeric, Enum 
from db.database import Base
from sqlalchemy.orm import relationship
from enum import Enum as PythonEnum
import sys
sys.path.append("C:\\Users\\Milto\\OneDrive\\Documentos\\Api_Multi\\db")



class Gender(PythonEnum):
    macho = "macho"
    hembra = "hembra"

class Species(PythonEnum):
    perro = "perro"
    gato = "gato"
    otro = "otro"

class Size(PythonEnum):
    pequeño = "pequeño"
    mediano = "mediano"
    grande = "grande"


class MascotasDb(Base):
    __tablename__ = 'mascotas'
    
    id_mascota = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    race = Column(String(50))
    weight = Column(Numeric(5, 2), nullable=False) 
    gender = Column(Enum(Gender), nullable=False) 
    species = Column(Enum(Species), nullable=False) 
    size = Column(Enum(Size), nullable=False)  
    image = Column(String(255))
    entity_id = Column(Integer, ForeignKey("entidad.id_entidad"), nullable=False)  


