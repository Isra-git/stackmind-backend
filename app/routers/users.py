""" 
EndPoint Users

"""
# app/routers/users.py

# dependencias
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.crud import user as crud_user
from app.schemas.user import UserResponse, UserUpdate

# creamos la instancia del router
router= APIRouter()

#endPoint para que un susuario elimine su propia cuenta (desctivo no borro)
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
        user_exists= crud_user.get_user_by_username(db, username=user_update.username)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario no esta disponible"
            )
    
    # actualizamos los datos
    user_data_update=crud_user.update_user(db=db, db_user=current_user, user_update=user_update)
    return user_data_update

