""" 
Funciones para crear cuenta, buscar a alguien por
su email o actualizar los puntos de respuesta

"""
# app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

# buscamos si ya existe un User con ese email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email==email).first()


# creamos User con passw haseada
def create_user(db: Session, user: UserCreate):
    
    # encriptamos passw
    hashed_password=get_password_hash(user.password)    

    # creamos el sechema de User para guardarlo en db
    db_user= User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        avatar_url=user.avatar_url,
        hashed_password=hashed_password
    )
    
    # lo añadimos -> Guardamos -> Actualizamos la sesión
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user