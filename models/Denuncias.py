from sqlalchemy import Integer, Column, ForeignKey, String, Text
from db.database import Base
from sqlalchemy.orm import relationship

class DenunciasDB(Base):
    __tablename__ = "denuncias"

    id_denuncias = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("users.id_user"), nullable=False)  
    motivo = Column(String, nullable=False)
    id_institucion = Column(Integer, ForeignKey("entidad.id_entidad"), nullable=False)
    descripcion = Column(Text, nullable=False)
    imagen = Column(String)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota"), nullable=False)
