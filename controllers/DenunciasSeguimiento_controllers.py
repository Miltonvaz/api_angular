from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.DenunciasSeguimientos_schemas import DenunciaSeguimientoRequest, DenunciaSeguimientoResponse
from models.DenunciasSeguimiento import DenunciasSeguimiento
from fastapi import APIRouter
import sys
sys.path.append("C:\\Users\\Milto\\OneDrive\\Documentos\\Api_Multi\\db")

seguimiento_router = APIRouter()

@seguimiento_router.post("/denuncias_seguimiento/", response_model=DenunciaSeguimientoResponse, status_code=status.HTTP_201_CREATED)
async def create_seguimiento(denuncia_seguimiento: DenunciaSeguimientoRequest, db: Session = Depends(get_db)):
    new_seguimiento = DenunciasSeguimiento(
        id_entidad=denuncia_seguimiento.id_entidad,
        fecha=denuncia_seguimiento.fecha,
        descripcion=denuncia_seguimiento.descripcion,
    )
    
    db.add(new_seguimiento)
    db.commit()
    db.refresh(new_seguimiento)
    
    return DenunciaSeguimientoResponse.from_orm(new_seguimiento)

@seguimiento_router.get("/denuncias_seguimiento/{denuncia_id}/", response_model=list[DenunciaSeguimientoResponse], status_code=status.HTTP_200_OK)
async def get_seguimientos(denuncia_id: int, db: Session = Depends(get_db)):
    seguimientos = db.query(DenunciasSeguimiento).filter(DenunciasSeguimiento.id_denuncia == denuncia_id).all()
    
    if not seguimientos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron seguimientos para esta denuncia")
    
    return [DenunciaSeguimientoResponse.from_orm(seguimiento) for seguimiento in seguimientos]

@seguimiento_router.get("/denuncias_seguimiento_all/", response_model=list[DenunciaSeguimientoResponse], status_code=status.HTTP_200_OK)
async def get_seguimientos_all(denuncia_id: int, db: Session = Depends(get_db)):
    seguimientos = db.query(DenunciasSeguimiento).filter(DenunciasSeguimiento.id_denuncia == denuncia_id).all()
    
    if not seguimientos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron seguimientos para esta denuncia")
    
    return [DenunciaSeguimientoResponse.from_orm(seguimiento) for seguimiento in seguimientos]

@seguimiento_router.put("/denuncias_seguimiento/{seguimiento_id}/", response_model=DenunciaSeguimientoResponse, status_code=status.HTTP_200_OK)
async def update_seguimiento(seguimiento_id: int, seguimiento_update: DenunciaSeguimientoRequest, db: Session = Depends(get_db)):
    seguimiento = db.query(DenunciasSeguimiento).filter(DenunciasSeguimiento.id_seguimiento == seguimiento_id).first()
    
    if not seguimiento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seguimiento no encontrado")
    
    for var, value in vars(seguimiento_update).items():
           if value is not None:  
            setattr(seguimiento, var, value)

    db.commit()
    db.refresh(seguimiento)

    return DenunciaSeguimientoResponse.from_orm(seguimiento)

@seguimiento_router.delete("/denuncias_seguimiento/{seguimiento_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seguimiento(seguimiento_id: int, db: Session = Depends(get_db)):
    seguimiento = db.query(DenunciasSeguimiento).filter(DenunciasSeguimiento.id_seguimiento == seguimiento_id).first()
    
    if not seguimiento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seguimiento no encontrado")
    
    db.delete(seguimiento)
    db.commit()

