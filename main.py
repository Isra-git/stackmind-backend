"""  
    ARCHIVO PRINCIPAL

"""
#main.py
# importamos las dependencias
from fastapi import FastAPI

from app.core.database import engine, Base
from app.models import user, question, answer
from app.routers import auth
from app.routers import questions

# Creamos las tablas en supabase de los modelos 
Base.metadata.create_all(bind=engine)

# Creamos la instancia de FastAPI
app = FastAPI(title="StackMind API by israDev")

# conectamos los Ruters con la instancia de FastAPI
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(questions.router, prefix="/questions", tags=["Questions"])



""" 
    ENDPOINTS

"""

# punto de Entrada
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de StackMind"}