""" 
Funciones para crear una respuesta, listar todas las respuestas

"""
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
