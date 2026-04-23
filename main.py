"""  
    ARCHIVO PRINCIPAL

"""
#main.py
# importamos las dependencias
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.models import user, question, answer

from app.routers import auth
from app.routers import questions
from app.routers import answers
from app.routers import users
from app.routers import ai
from app.routers import tags

# Creamos las tablas en supabase de los modelos 
Base.metadata.create_all(bind=engine)

# Creamos la instancia de FastAPI
app = FastAPI(title="StackMind API by israDev")

# configuracion CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://localhost:5173",
    "http://localhost:5174", # evita problemas cuando el puerto esta ocupado
        "http://127.0.0.1:5174",
        "https://stackmind-api.onrender.com",
    ], # todo -> Cambiar cuando tenga el front 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], # permitimos jwt
)

# conectamos los Ruters con la instancia de FastAPI
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(answers.router, prefix="/answers", tags=["Answers"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(ai.router, prefix="/ai", tags=["Artificial Intelligence"])
app.include_router(tags.router, prefix="/tags", tags=["Tags"])

""" 
    ENDPOINTS

"""

# punto de Entrada
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de StackMind"}