from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.security import hash_password, verify_password, create_access_token
from schemas import User_schemas
from models.User import UserDB,NombreCompleto
from db.database import get_db
from typing import List
from typing import Union
user_router = APIRouter()

@user_router.post("/registrer/", response_model=Union[User_schemas.UserOut,User_schemas.EntidadRegistrationResponse])
async def create_user(user: User_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado")

    hashed_password = hash_password(user.password)
    full_name = NombreCompleto(name=user.nombre_completo.name, last_name=user.nombre_completo.last_name)

    db_user = UserDB(
        email=user.email,
        password=hashed_password,
        rol=user.rol,
        name=full_name
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    if user.rol == "entidad":
        return User_schemas.EntidadRegistrationResponse(message="Usuario registrado. Por favor complete los datos de la entidad.", user_id=db_user.id_user)


    return User_schemas.UserOut(
        id_user=db_user.id_user,
        nombre_completo=f"{full_name.name} {full_name.last_name}",
        email=db_user.email,
        rol=db_user.rol
    )

@user_router.post("/login/", response_model=User_schemas.LoginResponse, status_code=status.HTTP_200_OK)
async def login(login_request: User_schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == login_request.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if not verify_password(login_request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    access_token = create_access_token(data={"sub": user.email})
    
    first_name = user.name.name
    last_name = user.name.last_name
    
    return User_schemas.LoginResponse(
        id_user=user.id_user, 
        name=first_name,
        lastName=last_name,  
        email=user.email, 
        rol=user.rol,
        access_token=access_token  
    )

@user_router.get("/users/listUsers/", response_model=List[User_schemas.UserOut])
async def list_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()

    users_response = []
    for user in users:
        full_name = f"{user.name.name} {user.name.last_name}"

        users_response.append(
            User_schemas.UserOut(
                id_user=user.id_user,
                nombre_completo=full_name,
                email=user.email,
                rol=user.rol,
            )
        )

    return users_response


@user_router.get("/users/{user_id}/", response_model=User_schemas.UserOut, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id_user == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
  
    full_name = f"{user.name.name} {user.name.last_name}"

    return User_schemas.UserOut(
        id_user=user.id_user,
        nombre_completo=full_name,  
        email=user.email,
        rol=user.rol
    )


@user_router.put("/users/{user_id}/", response_model=User_schemas.UserOut, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, update_request: User_schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id_user == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.name = f"{update_request.nombre_completo.name} {update_request.nombre_completo.last_name}"
    user.email = update_request.email

    if update_request.password:
        user.password = hash_password(update_request.password)
    
    if update_request.rol:
        user.rol = update_request.rol
    
    db.commit()
    db.refresh(user)
    
    return user


@user_router.delete("/users/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id_user == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(user)
    db.commit()
