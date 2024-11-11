from sqlalchemy import Integer, Column, ForeignKey, TIMESTAMP, Text
from db.database import Base
from sqlalchemy.orm import relationship
import sys
sys.path.append("C:\\Users\\Milto\\OneDrive\\Documentos\\Api_Multi\\db")

class DenunciasComentarios(Base):
    __tablename__ = "denuncias_comentarios"
    
    id_comentario = Column(Integer, primary_key=True)
    id_denuncia = Column(Integer, ForeignKey("denuncias.id_denuncias"), nullable=False)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    comentario = Column(Text, nullable=False)
    fecha = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")

 
