"""  
Gestionamos las contraseñas y los tokens

"""

from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
import os 
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User


# leemos el .env
load_dotenv()

# configuramos el hashing para las contraseñas
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")

# declaramos el tipo de seguridad
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Encriptamos la contraseña plana en un hash
def get_password_hash(password):
    return pwd_context.hash(password)


# Verificamos si la contraseña coincide con el hash 
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Creamos un Token JWT firmado  
def create_access_token(data: dict, expires_delta: timezone=None):
    # hacemos una copia de los datos
    to_encode=data.copy()
    
    # comprobamos si se paso un tiempo de expiracion especifico
    if expires_delta:
        expire=datetime.now(timezone.utc)+expires_delta
    else:
        #si no se pasa, le damos 30 minutos
        expire=datetime.now(timezone.utc)+timedelta(minutes=30)
    
    # añadimos la fecha de expiracion del token
    to_encode.update({"exp":expire})
    
    # haseamos el token
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    #devolvemos el token haseado
    return encoded_jwt

# funcion para comprobar el token y dar paso (Control Seguridad)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    # excepcion estandar para fallo al comprobar las credenciales
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pueden validar tus credenciales",
        headers={"www-Authenticate":"bearer"},
    )
    
    
    # intentamos leer el token Jtw
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        # si no se consigue
        if user_id is None:
            raise credentials_exception
    
    # si el token no es correcto o esta Expired
    except JWTError:
        raise credentials_exception
    
    # token ok, buscamos usuario
    user = db.query(User).filter(User.id == user_id).first()
    
    # si no hay usuario
    if user is None:
        raise credentials_exception
    
    return user


