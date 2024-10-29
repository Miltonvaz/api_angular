from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, SessionLocal

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://miltonvaz.github.io"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    id: int
    username: str
    email: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class Cars(BaseModel):
    id: int
    name: str
    model: str
    year: int
    price: int
    color: str
    description: str
    category: str

class PurchaseOrder(BaseModel):
    id: int
    user_id: int
    car_id: int
    date: str
    status: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register/", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
async def register_user(register_request: RegisterRequest, db: Session = Depends(get_db)):
    user_exists = db.query(models.LoginDB).filter(models.LoginDB.email == register_request.email).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario ya existe")
    
    new_user = models.LoginDB(
        username=register_request.username, 
        password=register_request.password,  
        email=register_request.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return LoginResponse(id=new_user.id, username=new_user.username, email=new_user.email)

@app.post("/login/", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.LoginDB).filter(models.LoginDB.email == login_request.email).first()
    if not user or user.password != login_request.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario o contraseña incorrectos")
    
    return LoginResponse(id=user.id, username=user.username, email=user.email)


@app.get("/listUsers/", response_model=List[LoginResponse], status_code=status.HTTP_200_OK)
async def consultar_user(db: Session = Depends(get_db)):
    users = db.query(models.LoginDB).all()
    return users


@app.get("/users/{user_id}", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.LoginDB).filter(models.LoginDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

@app.post("/cars/", response_model=Cars, status_code=status.HTTP_201_CREATED)
async def add_car(car: Cars, db: Session = Depends(get_db)):
    existing_car = db.query(models.CarsDB).filter(models.CarsDB.id == car.id).first()
    if existing_car:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El vehículo ya existe con el mismo ID")
    
    new_car = models.CarsDB(
        name=car.name,
        model=car.model,
        year=car.year,
        price=car.price,
        color=car.color,
        description=car.description,
        category=car.category
    )
    db.add(new_car)
    db.commit() 
    db.refresh(new_car)  
    return new_car


@app.get("/cars/{car_id}", response_model=Cars, status_code=status.HTTP_200_OK)
async def get_car_by_id(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.CarsDB).filter(models.CarsDB.id == car_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coche no encontrado")
    return car


@app.get("/allCars/", response_model=List[Cars], status_code=status.HTTP_200_OK)
async def consultar_car(db: Session = Depends(get_db)):
    cars = db.query(models.CarsDB).all()
    return cars

@app.put("/cars/{car_id}", response_model=Cars, status_code=status.HTTP_200_OK)
async def update_car(car_id: int, car: Cars, db: Session = Depends(get_db)):
    car_db = db.query(models.CarsDB).filter(models.CarsDB.id == car_id).first()
    if not car_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coche no encontrado")
    
    car_db.name = car.name
    car_db.model = car.model
    car_db.year = car.year
    car_db.price = car.price
    car_db.color = car.color
    car_db.description = car.description
    car_db.category = car.category
    
    db.commit()
    db.refresh(car_db)
    return car_db


@app.delete("/cars/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(car_id: int, db: Session = Depends(get_db)):
    car_db = db.query(models.CarsDB).filter(models.CarsDB.id == car_id).first()
    if not car_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coche no encontrado")
    
    db.delete(car_db)
    db.commit()
    return {"detail": "Coche eliminado exitosamente"}


@app.post("/purchaseOrder/", response_model=PurchaseOrder, status_code=status.HTTP_201_CREATED)
async def add_purchase_order(purchaseOrder: PurchaseOrder, db: Session = Depends(get_db)):
    new_purchase_order = models.PurchaseOrderDB(
        id=purchaseOrder.id,  
        user_id=purchaseOrder.user_id,
        car_id=purchaseOrder.car_id,
        date=purchaseOrder.date,
        status=purchaseOrder.status
    )
    db.add(new_purchase_order)
    db.commit()
    db.refresh(new_purchase_order)
    return new_purchase_order


@app.get("/purchaseOrder/{purchaseOrder_id}", response_model=PurchaseOrder, status_code=status.HTTP_200_OK)
async def get_purchase_order_by_id(purchaseOrder_id: int, db: Session = Depends(get_db)):
    purchase_order = db.query(models.PurchaseOrderDB).filter(models.PurchaseOrderDB.id == purchaseOrder_id).first()
    if not purchase_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden de compra no encontrada")
    return purchase_order


@app.put("/purchaseOrder/{purchaseOrder_id}", response_model=PurchaseOrder, status_code=status.HTTP_200_OK)
async def update_purchase_order(purchaseOrder_id: int, purchaseOrder: PurchaseOrder, db: Session = Depends(get_db)):
    purchase_order_db = db.query(models.PurchaseOrderDB).filter(models.PurchaseOrderDB.id == purchaseOrder_id).first()
    if not purchase_order_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden de compra no encontrada")
    
    purchase_order_db.user_id = purchaseOrder.user_id
    purchase_order_db.car_id = purchaseOrder.car_id
    purchase_order_db.date = purchaseOrder.date
    purchase_order_db.status = purchaseOrder.status
    
    db.commit()
    db.refresh(purchase_order_db)
    return purchase_order_db


@app.delete("/purchaseOrder/{purchaseOrder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_purchase_order(purchaseOrder_id: int, db: Session = Depends(get_db)):
    purchase_order_db = db.query(models.PurchaseOrderDB).filter(models.PurchaseOrderDB.id == purchaseOrder_id).first()
    if not purchase_order_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden de compra no encontrada")
    
    db.delete(purchase_order_db)
    db.commit()
    return {"detail": "Orden de compra eliminada exitosamente"}
