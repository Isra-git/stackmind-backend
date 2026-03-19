"""  
    ROUTER PARA AUTH / LOGIN

"""
# importamos las dependencias 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud import user as crud_user
from app.core.security import verify_password, create_access_token, get_current_user
from app.models.user import User

# Creamos la instancia de APIRouter
router = APIRouter()


# definimos la ruta de Registro de usuarios
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # comprobamos si existe el usuario
    db_user=crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El Email ya esta registrado")
    
    # sino-> Creamos el usuario en la db
    return crud_user.create_user(db=db, user=user)



# definimos la ruta para loguearse 
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends() , db: Session=Depends(get_db)):
    # buscamos si existe por mail (en OAuth2 username=email)
    user = crud_user.get_user_by_email(db, email=form_data.username)
    
    # miramos si el user y el passw son correctos 
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"www-authenticate": "bearer"},
        )
    
    # si todo es correcto, creamos el token Jwt
    acces_token = create_access_token(data={"sub": str(user.id)})
    
    # devolvemos el token, segun estandard
    return {"access_token": acces_token, "token_type": "bearer"}


# definimos una ruta que devuelve los datos del usuario (models.User)
# ruta Protegida
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user