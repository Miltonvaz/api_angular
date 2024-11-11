from sqlalchemy import String, Integer, Column, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship
import sys
sys.path.append("C:\\Users\\Milto\\OneDrive\\Documentos\\Api_Multi\\db")

class DonacionesDB(Base):
    __tablename__ = "donaciones"
    id_donacion = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id_user"))  
    cantidad = Column(String)
    fecha = Column(String)
    entidad_id = Column(Integer, ForeignKey("entidad.id_entidad"))
    comprobante = Column(String)
 

