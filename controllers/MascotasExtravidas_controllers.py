import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.MascotasExtraviadas_schemas import MascotasExtraviadaRequest, MascotasExtraviadasResponse
from models.Mascotas_Extraviadas import MascotasExtraviadasDb
from fastapi.responses import JSONResponse
from typing import List

load_dotenv()

HOST_URL = os.getenv("HOST_URL")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

mascotasE_router = APIRouter(prefix="/mascotas-extraviadas", tags=["Mascotas Extraviadas"])

@mascotasE_router.post("/mascotas/", response_model=MascotasExtraviadasResponse, status_code=status.HTTP_201_CREATED)
async def create_mascota_extraviada(mascota_request: MascotasExtraviadaRequest, file: List[UploadFile] = File(...), db: Session = Depends(get_db)):
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

    new_mascota = MascotasExtraviadasDb(
        nombre=mascota_request.nombre,
        raza=mascota_request.raza,
        edad=mascota_request.edad,
        sexo=mascota_request.sexo,
        especie=mascota_request.especie,
        telefono=mascota_request.telefono,
        direccion=mascota_request.direccion,
        fecha_extravio=mascota_request.fecha_extravio,
        fecha=mascota_request.fecha_publicacion,
        descripcion=mascota_request.descripcion,
        usuario=mascota_request.usuario,
        imagen=",".join(image_urls),
    )
    
    db.add(new_mascota)
    db.commit()
    db.refresh(new_mascota)
 
    return MascotasExtraviadasResponse(
        id=new_mascota.id_mascota_extraviada,  
        nombre=new_mascota.nombre,
        raza=new_mascota.raza,
        edad=new_mascota.edad,
        sexo=new_mascota.sexo,
        especie=new_mascota.especie,
        imagen=new_mascota.imagen,
        fecha_publicacion=new_mascota.fecha_publicacion,
        fecha_extravio=new_mascota.fecha_extravio,
        descripcion=new_mascota.descripcion,
    )

@mascotasE_router.get("/", response_model=list[MascotasExtraviadasResponse], status_code=status.HTTP_200_OK)
async def list_mascotas_extraviadas(db: Session = Depends(get_db)):
    mascotas = db.query(MascotasExtraviadasDb).all()
    return [
        MascotasExtraviadasResponse(
            id=mascota.id_mascota_extraviada,
            nombre=mascota.nombre,
            raza=mascota.raza,
            edad=mascota.edad,
            sexo=mascota.sexo,
            especie=mascota.especie,
            imagen=mascota.imagen,
            fecha_publicacion=mascota.fecha_publicacion,
            fecha_extravio=mascota.fecha_extravio,
            descripcion=mascota.descripcion
        ) for mascota in mascotas
    ]

@mascotasE_router.get("/{mascota_extraviada_id}/", response_model=MascotasExtraviadasResponse, status_code=status.HTTP_200_OK)
async def get_mascota_extraviada(mascota_extraviada_id: int, db: Session = Depends(get_db)):
    mascota = db.query(MascotasExtraviadasDb).filter(MascotasExtraviadasDb.id_mascota_extraviada == mascota_extraviada_id).first()
    
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota extraviada no encontrada")
    
    return MascotasExtraviadasResponse(
        id=mascota.id_mascota_extraviada, 
        nombre=mascota.nombre,
        raza=mascota.raza,
        edad=mascota.edad,
        sexo=mascota.sexo,
        especie=mascota.especie,
        imagen=mascota.imagen,
        fecha_publicacion=mascota.fecha_publicacion,
        fecha_extravio=mascota.fecha_extravio,
        descripcion=mascota.descripcion
    )

@mascotasE_router.put("/{mascota_extraviada_id}/", response_model=MascotasExtraviadasResponse, status_code=status.HTTP_200_OK)
async def update_mascota_extraviada(mascota_extraviada_id: int, mascota_update: MascotasExtraviadaRequest, db: Session = Depends(get_db)):
    mascota_extraviada = db.query(MascotasExtraviadasDb).filter(MascotasExtraviadasDb.id_mascota_extraviada == mascota_extraviada_id).first()
    
    if not mascota_extraviada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota extraviada no encontrada")
    
    mascota_extraviada.nombre = mascota_update.nombre
    mascota_extraviada.raza = mascota_update.raza
    mascota_extraviada.edad = mascota_update.edad
    mascota_extraviada.sexo = mascota_update.sexo
    mascota_extraviada.especie = mascota_update.especie
    mascota_extraviada.imagen = mascota_update.imagen
    mascota_extraviada.fecha_publicacion = mascota_update.fecha_publicacion
    mascota_extraviada.fecha_extravio = mascota_update.fecha_extravio
    mascota_extraviada.descripcion = mascota_update.descripcion

    db.commit()
    db.refresh(mascota_extraviada)    
    return MascotasExtraviadasResponse(
        id=mascota_extraviada.id_mascota_extraviada, 
        nombre=mascota_extraviada.nombre,
        raza=mascota_extraviada.raza,
        edad=mascota_extraviada.edad,
        sexo=mascota_extraviada.sexo,
        especie=mascota_extraviada.especie,
        imagen=mascota_extraviada.imagen,
        fecha_publicacion=mascota_extraviada.fecha_publicacion,
        fecha_extravio=mascota_extraviada.fecha_extravio,
        descripcion=mascota_extraviada.descripcion    
    )

@mascotasE_router.delete("/{mascota_extraviada_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mascota_extraviada(mascota_extraviada_id: int, db: Session = Depends(get_db)):
    mascota_extraviada = db.query(MascotasExtraviadasDb).filter(MascotasExtraviadasDb.id_mascota_extraviada == mascota_extraviada_id).first()
    if not mascota_extraviada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota extraviada no encontrada")
    
    db.delete(mascota_extraviada)
    db.commit()
    
    return {"detail": "Mascota extraviada eliminada con éxito"}
