""" 

   Endpoint para mostar los tags mas usados en las Preguntas


"""

# app/routers/tags.py

# dependencias
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.tag import TagResponse
from app.crud import tag as crud_tag


# definimos el router
router = APIRouter()

# endPOint que muestra los Tags mas populares
@router.get("/popular", response_model=List[TagResponse])
def get_popular_tags(limit: int = 10, db: Session = Depends(get_db)):
    # ordenándolos de mayor a menor.
    popular_tags=crud_tag.get_most_used_tags(db, limit=limit)
    return popular_tags

# enpoint para mostrar los Tags mas Nuevos
@router.get("/recent", response_model=List[TagResponse])
def get_recent_tags(limit: int = 12, db: Session = Depends(get_db)):
    # Simplemente ordenamos la tabla de Tags por fecha de creación descendente
    new_tags= crud_tag.get_latest_tags(db, limit=limit)
    return new_tags