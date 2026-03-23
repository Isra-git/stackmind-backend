"""
Funciones para crear una respuesta, listar todas las respuestas

"""
# app/crud/answers.py

# dependencias
from sqlalchemy.orm import Session

from app.models.answer import Answer
from app.schemas.answer import AnswerCreate, AnswerUpdate


# Funcion que crea una Respuesta
def create_answer(db: Session, answer: AnswerCreate, user_id: int, question_id: int):

    # creamos el modelo para la bd
    db_answer = Answer(
        body=answer.body,
        main_concept=answer.main_concept,
        author_id=user_id,
        question_id=question_id,
    )

    # lo guardamos en la BD
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)

    return db_answer


# Funcion que devuelve una Respuesta por su id
def get_answer(
    db: Session,
    answer_id: int,
):
    answer_by_id = db.query(Answer).filter(Answer.id == answer_id).first()
    return answer_by_id


# funcion que devuelve una lista de las Respuestas a una Pregunta por (question_id)
def get_answers_by_question(
    db: Session, question_id: int, skip: int = 0, limit: int = 100
):
    answer_list = (
        db.query(Answer)
        .filter(Answer.question_id == question_id)
        .order_by(Answer.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return answer_list

# Funcion que edita una Respuesta por su id
def update_answer(db: Session, db_answer: Answer, answer_update: AnswerUpdate):
    
    # scamos de Json solo los datos que el usuario ha -Enviado-
    update_data = answer_update.model_dump(exclude_unset=True)
    
    # actualizamos el objeto para la Bd campo x campo (solo los que edito)
    for key, value in update_data.items():
        setattr(db_answer, key, value)
    
    # guardamos los cambios en la bd
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    
    return db_answer



# Funcion que elimina una Respuesta por su Id
def delete_answer(db:Session,db_answer: Answer):
    
    db.delete(db_answer)
    db.commit()
    
    return(db_answer)
