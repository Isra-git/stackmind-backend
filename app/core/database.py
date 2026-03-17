"""  
Conexion con la base de datos

"""
# app/core/database.py

# dependecias
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# leemos el .env
load_dotenv()

# cojemos -> url de db desde el .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL","postgresql://postgres:password@localhost:5432/postgres")

# creamos el motor de la bd (1 para toda la app)
# pool_pre_ping=True-> Comprobamos si supabase ha cerrado la conexion por inactividad¡¡
engine=create_engine(
    
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True,
)

# conexion temporal para cada peticion
SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

# clase base de los modelos 
Base = declarative_base()

# funcion para abrir y cerrar conexiones en los routers, asegura que se 
#   cierre correctamente la bd tras cada peticion
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

