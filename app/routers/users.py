"""
EndPoint Users

"""
# app/routers/users.py

# dependencias
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import os
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.question import Question
from app.models.answer import Answer
from app.crud import user as crud_user
from app.schemas.user import UserResponse, UserUpdate, UserLeaderboard, UserStats
from app.schemas.question import PaginatedQuestionResponse
from app.schemas.answer import AnswerResponse,PaginatedAnswerResponse

# creamos la instancia del router
router = APIRouter()


# endPoint para que un susuario elimine su propia cuenta (desctivo no borro)
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # llamamos a la funcion que desactiva al usuario
    crud_user.soft_delete_user(db=db, db_user=current_user)

    # como eliminamos no devolvemos nada por convencion
    return None


# endPoint para que un User edite sus datos (email No Permitido)
@router.put("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_my_account(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Si quiere cambiar [username] comprobamos que este libre
    if user_update.username and user_update.username != current_user.username:
        user_exists = crud_user.get_user_by_username(db, username=user_update.username)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario no esta disponible",
            )

    # actualizamos los datos
    user_data_update = crud_user.update_user(
        db=db, db_user=current_user, user_update=user_update
    )
    return user_data_update

""" ----TODO -> Cambiar logica a Crud ----------"""
# endPoint para ver Mis Preguntas en el foro
@router.get("/me/questions", response_model=PaginatedQuestionResponse)
def get_my_questions(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # filtramos las preguntas donde el autor es el User actual
    my_questions = (
        db.query(Question)
        .filter(Question.author_id == current_user.id)
        .order_by(Question.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # contamos el total de Preguntas
    total = db.query(Question).filter(Question.author_id == current_user.id).count()


    # devolvemos el Resultado -> Total + List[QuestionResponse]
    return{"total":total, "items":my_questions}



""" ----TODO -> Cambiar logica a Crud ----------"""

# endPoint para ver Mis Respuestas en el foro
@router.get("/me/answers", response_model=PaginatedAnswerResponse)
def get_my_answers(
    skip:int=0,
    limit:int=20,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    # Filtramos las Respuesta donde el autor es el User actual
    my_answers = (
        db.query(Answer)
        .filter(Answer.author_id == current_user.id)
        .order_by(Answer.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # contamos el total de Respuestas del Usuario
    total=db.query(Answer).filter(Answer.author_id == current_user.id).count()
    return {"total": total, "items": my_answers}




# ------- endPoint para ADMIN
# Si el correo es el del admin -> is_admin:true
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@stackmind.com")


# enPoint para Listar Todos los usuarios
@router.get("/admin/list", response_model=List[UserResponse])
def get_admin_users_list(
    skip: int = 0,
    limit: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # comprobamos que es el ADMIN
    if current_user.email != ADMIN_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acceso Denegado"
        )

    # generamos la lista de usuarios y la devolvemos
    users_list = crud_user.get_users(db=db, skip=skip, limit=limit)
    return users_list


# endPoint para activar Desactivar un Usuario
@router.put("/{user_id}/toggle-status", status_code=status.HTTP_200_OK)
def ban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # si no es el Admin
    if current_user.email != ADMIN_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado"
        )

    # comprobamos que exista el usuario
    target_user = crud_user.get_user(db, user_id=user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    # comprobamos que no sea el propio ADMIN
    if target_user.email == ADMIN_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivar a este usuario",
        )

    # devolvemos el usuario activado o desactivado
    update_user = crud_user.toogle_user_state(db=db, db_user=target_user)
    user_state = "activado" if update_user.is_active else "desactivado"

    return {"message": f"Usuario {update_user.username} ha sido: {user_state}."}


# endpoint para devolver los 10 Users con mas votos
@router.get("/leaderboard", response_model=List[UserLeaderboard])
def get_top_users(db: Session = Depends(get_db)):
    top_users_by_rating = (
        db.query(User)
        .filter(User.is_active == True)
        .order_by(User.reputation)
        .limit(10)
        .all()
    )
    return top_users_by_rating


# endPoint para devolver las estadisticas del perfil /me/stats
@router.get("/me/stats", response_model=UserStats)
def get_my_profile_stats(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    # contamos las Preguntas
    total_questions = (
        db.query(Question).filter(Question.author_id == current_user.id).count()
    )

    # contamos las Respuestas
    total_answers = db.query(Answer).filter(Answer.author_id == current_user.id).count()

    # devolvemos las estadisticas
    return {
        "questions_count": total_questions,
        "answers_count": total_answers,
        "reputation": current_user.reputation,
    }
