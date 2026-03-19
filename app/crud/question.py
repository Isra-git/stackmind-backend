"""  

Funciones para guardar las preguntas, listar todas , las
mas recientes, buscar una pregunta por su id

"""

# app/crud/question.py

# dependencias
from sqlalchemy.orm import Session
from app.models.question import Question
from app.schemas.question import QuestionCreate

# Funcion que crea y guarda la pregunta del usuario
def create_question(db: Session, question: QuestionCreate, user_id: int):
    
    #contenedor de la pregunta
    db_question = Question(
        title= question.title,
        body = question.body,
        author_id = user_id
    )
    
    #guardamos en la bd
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    return db_question
