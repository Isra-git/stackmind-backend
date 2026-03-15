"""  
Gestionamos las contraseñas y los tokens

"""

from passlib.context import CryptContext
from datetime import datetime, timezone
from jose import jwt
import os 
from dotenv import load_dotenv

load_dotenv()

# configuramos el hashing para las contraseñas
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")

def get_password_hash(password):
    """ Encriptamos la contraseña plana en un hash  """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """ Verificamos si la contraseña coincide con el hash  """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timezone=None):
    """ Creamos un Token JWT firmado  """
    # hacemos una copia de los datos
    to_encode=data.copy()
    
    # comprobamos si se paso un tiempo de expiracion especifico
    if expires_delta:
        expire=datetime.utcnow()+expires_delta
    else:
        #si no se pasa, le damos 15 minutos
        expire=datetime.utcnow()+timezone(minutes=15)
    
    # añadimos la fecha de expiracion del token
    to_encode.update({"exp":expire})
    
    # haseamos el token
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    #devolvemos el token haseado
    return encoded_jwt

