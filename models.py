from sqlalchemy import String, Integer, Column, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class LoginDB(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class CarsDB(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    model = Column(String)
    year = Column(Integer)
    price = Column(String)
    color = Column(String)
    description = Column(String)  
    category = Column(String)  

class PurchaseOrderDB(Base):
    __tablename__ = 'purchase_order'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    car_id = Column(Integer, ForeignKey('cars.id'))
    date = Column(String) 
    status = Column(String)