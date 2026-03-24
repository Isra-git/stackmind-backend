""" 
EndPoint Users

"""
# app/routers/users.py

# dependencias
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.crud import user as crud_user

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