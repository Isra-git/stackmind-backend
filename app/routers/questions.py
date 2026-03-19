""" 

EndPoint Questions

"""
#app/routers/questions.py
# dependencias
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.question import QuestionCreate, QuestionResponse
from app.crud import question as crud_question
from app.core.security import get_current_user
from app.models.user import User

# definimos el router
router = APIRouter()

# endPoint para crear una pregunta
@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_new_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user : User = Depends(get_current_user) # se asegura autenticacion
):
    return crud_question.create_question(db=db, question=question, user_id=current_user.id)

