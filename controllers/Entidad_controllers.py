import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session
from db.database import get_db
from models.Entidad import EntidadDB
from schemas.Entidad_schemas import EntidadRequest, EntidadResponse
from models.User import UserDB
from typing import List
from fastapi.responses import JSONResponse

load_dotenv()


HOST_URL = os.getenv("HOST_URL")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

entidad_router = APIRouter()

@entidad_router.post("/entidades/{user_id}/", response_model=EntidadResponse, status_code=status.HTTP_201_CREATED)
async def create_entidad(user_id: int, entidad_request: EntidadRequest, file: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id_user == user_id).first()
    if not user or user.rol != "entidad":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario no válido para entidad")
    
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


    new_entidad = EntidadDB(
        name=entidad_request.name,
        address=entidad_request.address,
        description=entidad_request.description,
        type=entidad_request.type,
        cellphone=entidad_request.cellphone,
        image=",".join(image_urls),  
        social_networks=entidad_request.social_networks,
        id_user=user.id_user
    )

    db.add(new_entidad)
    db.commit()
    db.refresh(new_entidad)

    return EntidadResponse.from_orm(new_entidad)

@entidad_router.get("/entidades/{entidad_id}/", response_model=EntidadResponse, status_code=status.HTTP_200_OK)
async def get_entidad_by_id(entidad_id: int, db: Session = Depends(get_db)):
    entidad = db.query(EntidadDB).filter(EntidadDB.id_entity == entidad_id).first()
    if not entidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entidad no encontrada")
    
    return EntidadResponse.from_orm(entidad)

@entidad_router.get("/entidades/", response_model=list[EntidadResponse], status_code=status.HTTP_200_OK)
async def get_all_entidades(db: Session = Depends(get_db)):
    entidades = db.query(EntidadDB).all()
    return [EntidadResponse.from_orm(entidad) for entidad in entidades]

@entidad_router.put("/entidades/{entidad_id}/", response_model=EntidadResponse, status_code=status.HTTP_200_OK)
async def update_entidad(entidad_id: int, entidad_request: EntidadRequest, db: Session = Depends(get_db)):
    entidad = db.query(EntidadDB).filter(EntidadDB.id_entity == entidad_id).first()

    if not entidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entidad no encontrada")
  
    for key, value in entidad_request.dict().items():
        setattr(entidad, key, value)
    
    db.commit()
    db.refresh(entidad)
    
    return EntidadResponse.from_orm(entidad)

@entidad_router.delete("/entidad/{entidad_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entidad(entidad_id: int, db: Session = Depends(get_db)):
    entidad = db.query(EntidadDB).filter(EntidadDB.id_entity == entidad_id).first()
    if not entidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entidad no encontrada")
    
    db.delete(entidad)
    db.commit()
    return {"detail": "Entidad eliminada con éxito"}
