from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.DenunciasComentarios_schemas import DenunciasComentariosRequest, DenunciasComentariosResponse
from models.DenunciasComentarios import DenunciasComentarios
from fastapi import APIRouter
import sys
sys.path.append("C:\\Users\\Milto\\OneDrive\\Documentos\\Api_Multi\\db")

comentario_router = APIRouter()

@comentario_router.post("/denuncias_comentarios/", response_model=DenunciasComentariosResponse, status_code=status.HTTP_201_CREATED)
async def create_comentario(comentario_request: DenunciasComentariosRequest, db: Session = Depends(get_db)):
    new_comentario = DenunciasComentarios(
        id_denuncia=comentario_request.id_denuncia,
        id_user=comentario_request.id_user,
        comentario=comentario_request.comentario,
        fecha=comentario_request.fecha
    )
    
    db.add(new_comentario)
    db.commit()
    db.refresh(new_comentario)
    
    return DenunciasComentariosResponse.from_orm(new_comentario)

@comentario_router.get("/denuncias_comentarios/{denuncia_id}/", response_model=list[DenunciasComentariosResponse], status_code=status.HTTP_200_OK)
async def get_comentarios_by_denuncia(denuncia_id: int, db: Session = Depends(get_db)):
    comentarios = db.query(DenunciasComentarios).filter(DenunciasComentarios.id_denuncia == denuncia_id).all()
    
    if not comentarios:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron comentarios para esta denuncia")
    
    return [DenunciasComentariosResponse.from_orm(comentario) for comentario in comentarios]

@comentario_router.put("/denuncias_comentarios/{comentario_id}/", response_model=DenunciasComentariosResponse, status_code=status.HTTP_200_OK)
async def update_comentario(comentario_id: int, comentario_update: DenunciasComentariosRequest, db: Session = Depends(get_db)):
    comentario = db.query(DenunciasComentarios).filter(DenunciasComentarios.id_comentario == comentario_id).first()
    
    if not comentario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentario no encontrado")
    
    for var, value in vars(comentario_update).items():
        if value is not None:  
            setattr(comentario, var, value)

    db.commit()
    db.refresh(comentario)

    return DenunciasComentariosResponse.from_orm(comentario)

@comentario_router.delete("/denuncias_comentarios/{comentario_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comentario(comentario_id: int, db: Session = Depends(get_db)):
    comentario = db.query(DenunciasComentarios).filter(DenunciasComentarios.id_comentario == comentario_id).first()
    
    if not comentario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentario no encontrado")
    
    db.delete(comentario)
    db.commit()
