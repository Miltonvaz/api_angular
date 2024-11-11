from sqlalchemy import String, Integer, Column, ForeignKey, Date, Text, Enum
from db.database import Base
from sqlalchemy.orm import relationship
import enum
import sys
sys.path.append("C:\\Users\\Milto\\OneDrive\\Documentos\\Api_Multi\\db")

class Gender(enum.Enum):
    macho = 'macho'
    hembra = 'hembra'


class Species(enum.Enum):
    perro = 'perro'
    gato = 'gato'
    otros = 'otros'

class MascotasExtraviadasDb(Base):
    __tablename__ = "mascotas_extraviadas"
    
    id_mascota_extraviada = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    raza = Column(String(255), nullable=False)
    edad = Column(Integer, nullable=False)
    sexo = Column(Enum(Gender), nullable=False)  
    especie = Column(Enum(Species), nullable=False)  
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(255), nullable=False)
    fecha_extravio = Column(Date, nullable=False)
    fecha_publicacion = Column(Date, nullable=False)
    descripcion = Column(Text, nullable=False)
    imagen = Column(String(255), nullable=True)
    usuario_id = Column(Integer, ForeignKey('users.id_user'), nullable=True)

 