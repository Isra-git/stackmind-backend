""" 
Funciones para crear una respuesta, listar todas las respuestas

"""
# app/crud/answers.py

# dependencias
from sqlalchemy.orm import Session

from app.models.answer import Answer
from app.schemas.answer import AnswerCreate,AnswerResponse


# Funcion que crea una Respuesta
def create_answer(db: Session, answer: AnswerCreate, user_id: int, question_id: int):
    
    # creamos el modelo para la bd
    db_answer= Answer(
        body= answer.body,
        main_concept= answer.main_concept,
        author_id= user_id,
        question_id= question_id
    )
    
    # lo guardamos en la BD
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    
    return db_answer

#funcion que devuelve una lista de las Respuestas a una Pregunta por (question_id)
def get_answers_by_question(db:Session,question_id: int):
    return db.query(Answer).filter(Answer.question_id== question_id).order_by(Answer.created_at.asc()).all()


