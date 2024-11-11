import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.Denuncias_schemas import DenunciasRequest, DenunciasResponse
from models.Denuncias import DenunciasDB
from fastapi.responses import JSONResponse
from typing import List
from dotenv import load_dotenv


load_dotenv()

HOST_URL = os.getenv("HOST_URL", "http://localhost:8000")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

denuncias_router = APIRouter()

@denuncias_router.post("/denuncias/", response_model=DenunciasResponse, status_code=status.HTTP_201_CREATED)
async def create_denuncia(denuncia_request: DenunciasRequest, file: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    image_urls = []
    for uploaded_file in file:
        try:
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
            with open(file_path, "wb") as myfile:
                content = await uploaded_file.read()
                myfile.write(content)
            
            image_url = f"{HOST_URL}/{UPLOAD_DIR}/{uploaded_file.filename}"
            image_urls.append(image_url)
        except FileNotFoundError:
            return JSONResponse(content={"saved": False}, status_code=status.HTTP_404_NOT_FOUND)

    new_denuncia = DenunciasDB(
        id_usuario=denuncia_request.id_usuario,
        motivo=denuncia_request.motivo,
        id_institucion=denuncia_request.id_institucion,
        descripcion=denuncia_request.descripcion,
        imagen=",".join(image_urls),
        id_mascota=denuncia_request.id_mascota
    )
    
    db.add(new_denuncia)
    db.commit()
    db.refresh(new_denuncia)
    
    return DenunciasResponse(
        id_denuncia=new_denuncia.id_denuncias,
        id_user=new_denuncia.id_usuario,
        motivo=new_denuncia.motivo,
        id_institucion=new_denuncia.id_institucion,
        descripcion=new_denuncia.descripcion,
        imagen=new_denuncia.imagen,
        id_mascota=new_denuncia.id_mascota
    )

@denuncias_router.get("/denuncias_all/", response_model=list[DenunciasResponse], status_code=status.HTTP_200_OK)
async def list_denuncias(db: Session = Depends(get_db)):
    denuncias = db.query(DenunciasDB).all()
    return [
        DenunciasResponse(
            id_denuncia=denuncia.id_denuncias,
            id_user=denuncia.id_usuario,
            motivo=denuncia.motivo,
            id_institucion=denuncia.id_institucion,
            descripcion=denuncia.descripcion,
            imagen=denuncia.imagen,
            id_mascota=denuncia.id_mascota
        ) for denuncia in denuncias
    ]

@denuncias_router.get("/denuncias/{denuncias_id}/", response_model=DenunciasResponse, status_code=status.HTTP_200_OK)
async def get_denuncia(denuncias_id: int, db: Session = Depends(get_db)):
    denuncia = db.query(DenunciasDB).filter(DenunciasDB.id_denuncias == denuncias_id).first()
    
    if not denuncia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Denuncia no encontrada")
    
    return DenunciasResponse(
        id_denuncia=denuncia.id_denuncias,
        id_user=denuncia.id_usuario,
        motivo=denuncia.motivo,
        id_institucion=denuncia.id_institucion,
        descripcion=denuncia.descripcion,
        imagen=denuncia.imagen,
        id_mascota=denuncia.id_mascota  
    )

@denuncias_router.put("/denuncias/{denuncias_id}/", response_model=DenunciasResponse, status_code=status.HTTP_200_OK)
async def update_denuncia(denuncias_id: int, denuncia_update: DenunciasRequest, db: Session = Depends(get_db)):
    denuncia = db.query(DenunciasDB).filter(DenunciasDB.id_denuncias == denuncias_id).first()
    
    if not denuncia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Denuncia no encontrada")
    
    denuncia.id_usuario = denuncia_update.id_usuario
    denuncia.motivo = denuncia_update.motivo
    denuncia.id_institucion = denuncia_update.id_institucion
    denuncia.descripcion = denuncia_update.descripcion
    denuncia.id_mascota = denuncia_update.id_mascota
    denuncia.imagen = ",".join(denuncia_update.imagen) 

    db.commit()
    db.refresh(denuncia)    

    return DenunciasResponse(
        id_denuncia=denuncia.id_denuncias,
        id_user=denuncia.id_usuario,
        motivo=denuncia.motivo,
        id_institucion=denuncia.id_institucion,
        descripcion=denuncia.descripcion,
        imagen=denuncia.imagen,
        id_mascota=denuncia.id_mascota
    )

@denuncias_router.delete("/denuncias/{denuncias_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_denuncia(denuncias_id: int, db: Session = Depends(get_db)):
    denuncia = db.query(DenunciasDB).filter(DenunciasDB.id_denuncias == denuncias_id).first()
    
    if not denuncia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Denuncia no encontrada")
    
    db.delete(denuncia)
    db.commit()
