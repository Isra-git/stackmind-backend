"""

EndPoint  Respuestas

"""

# app/routers/answers.py
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import os

from app.core.database import get_db
from app.schemas.answer import AnswerCreate, AnswerResponse, AnswerUpdate, AnswerVote
from app.crud import answer as crud_answer
from app.crud import question as crud_question
from app.core.security import get_current_user
from app.models.user import User
from app.models.answer import Answer
from app.utils.tags_utils import generar_tags_automaticos


# email del ADmin
ADMIN_EMAIL= os.getenv("ADMIN_EMAIL", "admin@stackmind.com")


# instancia del Router
router = APIRouter()


# endPoint para publicar una Respuesta (Protegida)
@router.post(
    "/question/{question_id}",
    response_model=AnswerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_answer(
    question_id: int,
    answer: AnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # comprobamos que existe la pregunta
    question = crud_question.get_question(db=db, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La pregunta que intentas responder no existe",
        )

    # Generamos los TAGS leyendo el array JSON de la respuesta
    tags = generar_tags_automaticos(answer.body)
    answer.main_concept=tags

    # si existe la pregunta, guardamos la respuesta
    return crud_answer.create_answer(
        db=db, answer=answer, user_id=current_user.id, question_id=question_id
    )


# endPoint para listar todas las Respuestas de una Pregunta (Publica)
@router.get(
    "/question/{question_id}",
    response_model=List[AnswerResponse],
    status_code=status.HTTP_200_OK,
)
def read_answers_from_question(
    question_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    # comprobamos que la pregunta existe
    question = crud_question.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La pregunta que intentas responder no existe",
        )

    # si existe devolvemos List [AnswerResponse]
    answer_for_question = crud_answer.get_answers_by_question(
        db=db, question_id=question_id, skip=skip, limit=limit
    )

    return answer_for_question


# endPoint para Actualizar una Respuesta
@router.put(
    "/{answer_id}", response_model=AnswerResponse, status_code=status.HTTP_200_OK
)
def update_answer(
    answer_id: int,
    answer_input: AnswerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # comprobamos que la Respuesta Existe
    db_answer = crud_answer.get_answer(db, answer_id=answer_id)
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La respuesta que intentas borrar no existe",
        )

    # comprobamos que es el Propietario de la Respuesta
    if db_answer.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar la respuesta",
        )

    # Si existe y es el Propietario de la Respuesta la actualizamos
    return crud_answer.update_answer(
        db=db, db_answer=db_answer, answer_update=answer_input
    )


# endPoint para eliminar una respuesta
@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # comprobamos que la Respuesta existe
    db_answer = crud_answer.get_answer(db=db, answer_id=answer_id)
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Respuesta no encontrada"
        )

    # comprobamos que es el Popietario de la Respuesta
    if db_answer.author_id != current_user.id and current_user.email != ADMIN_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar la respuesta",
        )

    # borramos la Respuesta
    crud_answer.delete_answer(db, db_answer)

    return None
# endPoint para Votar una Respuesta (protegido)
@router.post(
    "/{answer_id}/vote", response_model=AnswerResponse, status_code=status.HTTP_200_OK
)
def vote_answer(
    answer_id: int,
    vote: AnswerVote,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Comprobamos que la Respuesta existe
    db_answer = crud_answer.get_answer(db, answer_id)
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="La Respuesta NO existe"
        )

    #  LA REGLA ESTRICTA: Solo el autor de la pregunta puede votar
    # respuesta ->  pregunta -> a su autor
    if db_answer.question.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el creador de la pregunta original puede valorar las respuestas",
        )

    # Si es el autor, enviamos los puntos al CRUD para que calcule y guarde
    return crud_answer.vote_answer(db=db, db_answer=db_answer, score=vote.score)



# endPoint para devolver una Respuesta por su ID -> Para editarla
@router.get(
    "/{answer_id}", 
    response_model=AnswerResponse, 
    status_code=status.HTTP_200_OK
)
def get_answer(
    answer_id: int, 
    db: Session = Depends(get_db)
):
    # Llamamos al la funcion del Crud
    db_answer = crud_answer.get_answer(db=db, answer_id=answer_id)
    
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Respuesta no encontrada"
        )
        
    return db_answer