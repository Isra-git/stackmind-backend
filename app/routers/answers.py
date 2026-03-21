"""  

EndPoint  Respuestas

"""

# app/routers/answers.py
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.answer import AnswerCreate, AnswerResponse
from app.crud import answer as crud_answer
from app.crud import question as crud_question
from app.core.security import get_current_user
from app.models.user import User

# instancia del Router
router = APIRouter

# endPoint para publicar una Respuesta (Protegida)
@router.post("/question/{question_id}",response_model=AnswerResponse,status_code=status.HTTP_201_CREATED)
def create_new_answer(question_id:int,answer: AnswerCreate ,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    # comprobamos que existe la pregunta
    question = crud_question.get_question(db=db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="La pregunta que intentas responder no existe")
    
    # si existe la pregunta, guardamos la respuesta
    return crud_answer.create_answer(db=db, answer= answer, user_id=current_user.id, question_id=question_id)



# endPoint para listar todas las Respuestas de una Pregunta (Publica)
@router.get("/question/{question_id}", response_model=List[AnswerResponse],status_code=status.HTTP_200_OK)
def read_answers_from_question(question_id: int, db: Session = Depends(get_db)):
    return crud_answer.get_answers_by_question(db=db, question_id=question_id)