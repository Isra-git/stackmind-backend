""" 

EndPoint Questions

"""
#app/routers/questions.py
# dependencias
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.question import QuestionCreate, QuestionResponse
from app.crud import question as crud_question
from app.core.security import get_current_user
from app.models.user import User

# definimos el router
router = APIRouter()

# endPoint para crear una pregunta (solo para autenticados)
@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_new_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user : User = Depends(get_current_user) # se asegura autenticacion
):
    return crud_question.create_question(db=db, question=question, user_id=current_user.id)


# endPoint para leer preguntas (acceso publico)
@router.get("/", response_model=List[QuestionResponse])
def read_questions(skip: int=0, limit: int = 100, db: Session = Depends(get_db)):
    questions = crud_question.get_questions(db, skip=skip, limit=limit)
    return questions


# endPoint para ver una pregunta por su id (acceso publico)
@router.get("/{question_id}", response_model=QuestionResponse)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud_question.get_question(db, question_id=question_id)
    
    # si no encuentra el id , lanzamos excepcion 404
    if db_question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta no encontrada")
   
   # devolvemos la pregunta
    return db_question

