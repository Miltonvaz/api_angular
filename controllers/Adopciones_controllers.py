from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.Adopciones import AdopcionesDB  
from schemas.Adopciones_schemas import AdopcionRequest, AdopcionResponse  
from fastapi import APIRouter

adopciones_router = APIRouter()


@adopciones_router.post("/", response_model=AdopcionResponse, status_code=status.HTTP_201_CREATED)
async def create_adopcion(adopcion_request: AdopcionRequest, db: Session = Depends(get_db)):
    new_adopcion = AdopcionesDB(
        id_mascota=adopcion_request.id_mascota,
        id_usuario=adopcion_request.id_usuario,
        fecha_adopcion=adopcion_request.fecha_adopcion,
        curp=adopcion_request.curp,
        imagen=adopcion_request.imagen,
        seguimiento=adopcion_request.seguimiento,
        observaciones=adopcion_request.observaciones,
        adopcion = adopcion_request.status,
        condiciones=adopcion_request.condiciones
    )
    
    db.add(new_adopcion)
    db.commit()
    db.refresh(new_adopcion)
    
    return AdopcionResponse(
        id_mascota=new_adopcion.id_mascota,
        id_usuario=new_adopcion.id_usuario,
        fecha_adopcion=new_adopcion.fecha_adopcion,
        curp=new_adopcion.curp,
        imagen=new_adopcion.imagen,
        seguimiento=new_adopcion.seguimiento,
        observaciones=new_adopcion.observaciones,
        adopcion = new_adopcion.status,
        condiciones=new_adopcion.condiciones
    )

@adopciones_router.get("/all/", response_model=list[AdopcionResponse], status_code=status.HTTP_200_OK)
async def list_adopciones(db: Session = Depends(get_db)):
    adopciones = db.query(AdopcionesDB).all()
    return [
        AdopcionResponse(
            id_mascota=adopcion.id_mascota,
            id_usuario=adopcion.id_usuario,
            fecha_adopcion=adopcion.fecha_adopcion,
            curp=adopcion.curp,
            imagen=adopcion.imagen,
            seguimiento=adopcion.seguimiento,
            observaciones=adopcion.observaciones,
            adopcion = adopcion.status,
            condiciones=adopcion.condiciones
        ) for adopcion in adopciones
    ]

@adopciones_router.get("/{adopcion_id}/", response_model=AdopcionResponse, status_code=status.HTTP_200_OK)
async def get_adopcion(adopcion_id: int, db: Session = Depends(get_db)):
    adopcion = db.query(AdopcionesDB).filter(AdopcionesDB.id_adopcion == adopcion_id).first()
    
    if not adopcion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Adopcion no encontrada")
    
    return AdopcionResponse(
        id_mascota=adopcion.id_mascota,
        id_usuario=adopcion.id_usuario,
        fecha_adopcion=adopcion.fecha_adopcion,
        curp=adopcion.curp,
        imagen=adopcion.imagen,
        seguimiento=adopcion.seguimiento,
        observaciones=adopcion.observaciones,
        adopcion = adopcion.status,
        condiciones=adopcion.condiciones
    )

@adopciones_router.put("/{adopcion_id}/", response_model=AdopcionResponse, status_code=status.HTTP_200_OK)
async def update_adopcion(adopcion_id: int, adopcion_update: AdopcionRequest, db: Session = Depends(get_db)):
    adopcion = db.query(AdopcionesDB).filter(AdopcionesDB.id_adopcion == adopcion_id).first()
    
    if not adopcion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Adopcion no encontrada")
    
    adopcion.id_mascota = adopcion_update.id_mascota
    adopcion.id_usuario = adopcion_update.id_usuario
    adopcion.fecha_adopcion = adopcion_update.fecha_adopcion
    adopcion.curp = adopcion_update.curp
    adopcion.imagen = adopcion_update.imagen
    adopcion.seguimiento = adopcion_update.seguimiento
    adopcion.observaciones = adopcion_update.observaciones
    adopcion.status = adopcion_update.status
    adopcion.condiciones = adopcion_update.condiciones

    db.commit()
    db.refresh(adopcion)

    return AdopcionResponse(
        id_mascota=adopcion.id_mascota,
        id_usuario=adopcion.id_usuario,
        fecha_adopcion=adopcion.fecha_adopcion,
        curp=adopcion.curp,
        imagen=adopcion.imagen,
        seguimiento=adopcion.seguimiento,
        observaciones=adopcion.observaciones,
        adopcion = adopcion.status,
        condiciones=adopcion.condiciones
    )

@adopciones_router.delete("/{adopcion_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_adopcion(adopcion_id: int, db: Session = Depends(get_db)):
    adopcion = db.query(AdopcionesDB).filter(AdopcionesDB.id_adopcion == adopcion_id).first()
    
    if not adopcion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Adopcion no encontrada")
    
    db.delete(adopcion)
    db.commit()
    return {"detail": "Adopcion eliminada con éxito"}

