from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.Donaciones_schemas import DonacionesRequest, DonacionesResponse
from models.Donaciones import DonacionesDB
from fastapi import APIRouter
import sys
sys.path.append("C:\\Users\\Milto\\OneDrive\\Documentos\\Api_Multi\\db")
app = FastAPI()
donaciones_router = APIRouter()

@donaciones_router.post("/donaciones/", response_model=DonacionesResponse, status_code=status.HTTP_201_CREATED)
async def create_donacion(donacion_request: DonacionesRequest, db: Session = Depends(get_db)):
    new_donacion = DonacionesDB(
        id_user=donacion_request.user_id,
        cantidad=donacion_request.cantidad,
        fecha=donacion_request.fecha,
        entidad_id=donacion_request.entidad_id,
        comprobante=donacion_request.comprobante
    )
    
    db.add(new_donacion)
    db.commit()
    db.refresh(new_donacion)
    
    return DonacionesResponse(
        id_donacion=new_donacion.id_donacion,
        id_user=new_donacion.id_user,
        cantidad=new_donacion.cantidad,
        fecha=new_donacion.fecha,
        entidad_id=new_donacion.entidad_id,
        comprobante=new_donacion.comprobante
    )

@donaciones_router.get("/donaciones_all/", response_model=list[DonacionesResponse], status_code=status.HTTP_200_OK)
async def list_donaciones(db: Session = Depends(get_db)):
    donaciones = db.query(DonacionesDB).all()
    return [
        DonacionesResponse(
            id_user=donacion.id_user,
            cantidad=donacion.cantidad,
            fecha=donacion.fecha,
            entidad_id=donacion.entidad_id,
            comprobante=donacion.comprobante
        ) for donacion in donaciones
    ]

@donaciones_router.get("/donaciones/{donaciones_id}/", response_model=DonacionesResponse, status_code=status.HTTP_200_OK)
async def get_donaciones(donaciones_id: int, db: Session = Depends(get_db)):
    donacion = db.query(DonacionesDB).filter(DonacionesDB.id_donacion == donaciones_id).first()
    
    if not donacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donación no encontrada")
    
    return DonacionesResponse(
        id_user=donacion.id_user,
        cantidad=donacion.cantidad,
        fecha=donacion.fecha,
        entidad_id=donacion.entidad_id,
        comprobante=donacion.comprobante
    )

@donaciones_router.put("/donaciones/{donaciones_id}/", response_model=DonacionesResponse, status_code=status.HTTP_200_OK)
async def update_donacion(donaciones_id: int, donacion_update: DonacionesRequest, db: Session = Depends(get_db)):
    donacion = db.query(DonacionesDB).filter(DonacionesDB.id_donacion == donaciones_id).first()
    
    if not donacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donación no encontrada")

    donacion.id_user = donacion_update.user_id
    donacion.cantidad = donacion_update.cantidad
    donacion.fecha = donacion_update.fecha
    donacion.entidad_id = donacion_update.entidad_id
    donacion.comprobante = donacion_update.comprobante

    db.commit()
    db.refresh(donacion)    

    return DonacionesResponse(
        id_user=donacion.id_user,
        cantidad=donacion.cantidad,
        fecha=donacion.fecha,
        entidad_id=donacion.entidad_id,
        comprobante=donacion.comprobante
    )

@donaciones_router.delete("/donaciones/{donacion_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_donacion(donacion_id: int, db: Session = Depends(get_db)):
    donacion = db.query(DonacionesDB).filter(DonacionesDB.id_donacion == donacion_id).first()
    if not donacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donación no encontrada")
    
    db.delete(donacion)
    db.commit()
    return {"detail": "Donación eliminada con éxito"}


