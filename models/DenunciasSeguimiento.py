from sqlalchemy import String, Integer, Column, ForeignKey, TIMESTAMP, Text
from db.database import Base
from sqlalchemy.orm import relationship
import sys
sys.path.append("C:\\Users\\Milto\\OneDrive\\Documentos\\Api_Multi\\db")

class DenunciasSeguimiento(Base):
    __tablename__ = "denuncias_seguimiento"
    
    id_seguimiento = Column(Integer, primary_key=True)
    id_denuncia = Column(Integer, ForeignKey("denuncias.id_denuncias"), nullable=False)
    id_entidad = Column(Integer, ForeignKey("entidad.id_entidad"), nullable=True)
    fecha = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    descripcion = Column(Text, nullable=False)
