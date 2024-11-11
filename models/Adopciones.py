from sqlalchemy import String, Integer, Column, ForeignKey, Enum
from db.database import Base
from sqlalchemy.orm import relationship
import enum
import sys
sys.path.append("C:\\Users\\Milto\\OneDrive\\Documentos\\Api_Multi\\db")


class StatusAdoption(enum.Enum):
    rechazado = 'rechazado'
    proceso = 'proceso'
    aceptado = 'aceptado'


class AdopcionesDB(Base):
    __tablename__ = 'adopciones'
    
    id_adopcion = Column(Integer, primary_key=True)
    id_mascota = Column(Integer, ForeignKey('mascotas.id_mascota'), nullable=False)  
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False) 
    fecha_adopcion = Column(String, nullable=False) 
    curp = Column(String)
    imagen = Column(String)
    status = Column(String, nullable=False)  
    seguimiento = Column(String)
    observaciones = Column(String)
    condiciones = Column(String)