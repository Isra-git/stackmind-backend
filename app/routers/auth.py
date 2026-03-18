"""  
    ROUTER PARA AUTH / LOGIN

"""
# importamos las dependencias
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud import user as crud_user

# Creamos la instancia de APIRouter
router = APIRouter()

# definimos la ruta de Registro de usuarios
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # comprobamos si existe el usuario
    db_user=crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El Email ya esta registrado")
    
    # sino-> Creamos el usuario en la db
    return crud_user.create_user(db=db, user=user)

@router.post("/login")
def login(user_data: UserCreate, db: Session=Depends(get_db)):
    # TODO -> lOGICA DE VALIDACION DE PASSWD Y GENERAR JWT
    pass
