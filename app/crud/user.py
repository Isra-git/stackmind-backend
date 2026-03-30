""" 
Funciones para crear cuenta, buscar a alguien por
su email o actualizar los puntos de respuesta

"""
# app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate,UserUpdate
from app.core.security import get_password_hash

# buscamos si ya existe un User con ese email
def get_user_by_email(db: Session, email: str):
    user_by_email = db.query(User).filter(User.email==email).first()
    return user_by_email

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


# Funcion para dar de baja (is_active:False) a un User
def soft_delete_user(db: Session, db_user: User):
    
    # Sobreescribimos Todos sus datos
    db_user.email = f"deleted_user{db_user.id}@stackmind.mock"
    db_user.username = f"deleted_uuser{db_user.id}"
    db_user.full_name = "Deleted User"
    db_user.avatar_url = None
    db_user.hashed_password = "disables_account"
    # lo damos de baja ( is_active:false)
    db_user.is_active = False
    
    # guardamos los cambios
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # devolvemos los mock__datos del usuario dado de baja
    return db_user

# funcion para buscar si un Alias ya esta usado
def get_user_by_username(db: Session, username:str):
    user_is_used=db.query(User).filter(User.username== username).first()
    return user_is_used

# Funcion para Modificar los datos de un User
def update_user(db: Session, db_user: User, user_update: UserUpdate):
    
    # sacamos los datos en Json que ha cambiado
    update_data = user_update.model_dump(exclude_unset=True)
    
    # actualizamos los campos del usuario
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    # guardamos los datos del usuario
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # devolvemos los nuevos datos del usuario
    return db_user


# funcion para Listar los usuarios ordenados por Rating Desc
def get_all_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
):
    # realizamos la consulta
    users=db.query(User)\
        .filter(User.is_active)\
        .order_by(User.reputation.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    # devolvemos la lista de usuarios
    return users

# Funcion que devuelve un Usuario por su ID
def get_user(
    db: Session,
    user_id: int
):
    user = db.query(User).filter(User.id==user_id).first()
    return user


# Funcion que devuelve una lista completa de usuarios (para el ADMIn)
def get_users(
    db: Session,
    skip: int = 0 ,
    limit : int = 100
):
    users_list=db.query(User).offset(skip).limit(limit).all()
    return users_list

# Alterna el estado is_active de un Usuario
def toogle_user_state(
    db: Session,
    db_user:User
):
    # invertimos el estado del booleano _is_active_
    db_user.is_active = not db_user.is_active
    db.commit()
    db.refresh(db_user)
    return db_user