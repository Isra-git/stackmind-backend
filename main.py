"""  
    ARCHIVO PRINCIPAL

"""
#main.py
# importamos las dependencias
from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import user, question, answer
from app.routers import auth

#from app.routers import auth

# Creamos las tablas en supabase de los modelos 
Base.metadata.create_all(bind=engine)

# Creamos la instancia de FastAPI
app = FastAPI(title="StackMind API")

# conectamos el modulo de autenticacion con la instancia de FastAPI
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


""" 
    ENDPOINTS

"""
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de StackMind"}