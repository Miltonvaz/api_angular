import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.Mascotas import MascotasRequest, MascotasResponse
from models.Mascotas import MascotasDb
from typing import List
from fastapi.responses import JSONResponse

load_dotenv()

HOST_URL = os.getenv("HOST_URL")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

mascota_router = APIRouter()

@mascota_router.post("/mascotas/", response_model=MascotasResponse, status_code=status.HTTP_201_CREATED)
async def create_mascota(request: Request, mascota_request: MascotasRequest, file: List[UploadFile] = File(...), db: Session = Depends(get_db)):
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

    new_mascota = MascotasDb(
        nombre=mascota_request.name,
        raza=mascota_request.race,
        edad=mascota_request.age,
        sexo=mascota_request.gender,
        especie=mascota_request.species,
        peso=mascota_request.weight,
        tamaño=mascota_request.size,
        imagen=",".join(image_urls), 
        entidad=mascota_request.entity_id
    )
    db.add(new_mascota)
    db.commit()
    db.refresh(new_mascota)

    return MascotasResponse(
        nombre=new_mascota.name,
        raza=new_mascota.race,
        edad=new_mascota.age,
        sexo=new_mascota.gender,
        especie=new_mascota.species,
        peso=new_mascota.weight,
        tamaño=new_mascota.size,
        imagen=new_mascota.image,
        entidad=new_mascota.entity_id
    )


@mascota_router.get("/mascotas_all/", response_model=list[MascotasResponse], status_code=status.HTTP_200_OK)
async def list_mascotas(db: Session = Depends(get_db)):
    mascotas = db.query(MascotasDb).all()
    return [
        MascotasResponse(
            nombre=mascota.name,
            raza=mascota.race,
            edad=mascota.age,
            sexo=mascota.gender,
            especie=mascota.species,
            peso=mascota.weight,
            tamaño=mascota.size,
            imagen=mascota.image,
            entidad=mascota.entity_id
        ) for mascota in mascotas
    ]

@mascota_router.get("/mascotas/{mascota_id}/", response_model=MascotasResponse, status_code=status.HTTP_200_OK)
async def get_mascota(mascota_id: int, db: Session = Depends(get_db)):
    mascota = db.query(MascotasDb).filter(MascotasDb.id_mascotas == mascota_id).first()
    
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
    
    return MascotasResponse(
        nombre=mascota.name,
        raza=mascota.race,
        edad=mascota.age,
        sexo=mascota.gender,
        especie=mascota.species,
        peso=mascota.weight,
        tamaño=mascota.size,
        imagen=mascota.image,
        entidad=mascota.entity_id
    )

@mascota_router.put("/mascotas/{mascota_id}/", response_model=MascotasResponse, status_code=status.HTTP_200_OK)
async def update_mascota(mascota_id: int, mascota_update: MascotasRequest, db: Session = Depends(get_db)):
    mascota = db.query(MascotasDb).filter(MascotasDb.id_mascotas == mascota_id).first()
    
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
    
    mascota.name = mascota_update.name
    mascota.race = mascota_update.race
    mascota.age = mascota_update.age
    mascota.gender = mascota_update.gender
    mascota.species = mascota_update.species
    mascota.weight = mascota_update.weight
    mascota.size = mascota_update.size
    mascota.image = mascota_update.image
    mascota.entity_id = mascota_update.entity_id

    db.commit()
    db.refresh(mascota)
    
    return MascotasResponse(
        nombre=mascota.name,
        raza=mascota.race,
        edad=mascota.age,
        sexo=mascota.gender,
        especie=mascota.species,
        peso=mascota.weight,
        tamaño=mascota.size,
        imagen=mascota.image,
        entidad=mascota.entity_id
    )

@mascota_router.delete("/mascotas/{mascota_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mascota(mascota_id: int, db: Session = Depends(get_db)):
    mascota = db.query(MascotasDb).filter(MascotasDb.id_mascotas == mascota_id).first()
    
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
    
    db.delete(mascota)
    db.commit()
    
    return {"detail": "Mascota eliminada con éxito"}
