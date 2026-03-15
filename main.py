"""  
    ARCHIVO PRINCIPAL

"""

# importamos las dependencias
from fastapi import FastAPI
from .database import engine, Base
from .models import user 
from .routers import auth

# Creamos las tablas en supabase de los modelos 
Base.metadata.create_all(bind=engine)

# Creamos la instancia de FastAPI
app = FastAPI()

# conectamos el modulo de autenticacion con la instancia de FastAPI
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


""" 
    ENDPOINTS

"""
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de StackMind"}