""" 

    Extraemos los Tags de las Respuestas


"""

#app/crud/tag.py

# dependencias
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.answer import Answer

# Funcion para Devolver los Tags + Usados
def get_most_used_tags(
    db: Session,
    limit: int = 10
):
    # hacemos una consulta agrupando por [main_concept] y contando los que hay
    results=(
        db.query(
        Answer.main_concept.label("name"),
        func.count(Answer.id).label("counter")
    )
    .filter(Answer.main_concept.isnot(None)) # No Respuestas sin Tags
    .group_by(Answer.main_concept) # Agrupados por Repetidos
    .order_by(func.count(Answer.id).desc()) # Ordenamos de Mayor a Menor
    .limit(limit)
    .all()
    )
    
    # results devuelve una Tupla -> la convertimos en Dict
    resultado =[{"name": row.name, "counter": row.counter} for row in results]
    
    # devolvemos el resultado
    return resultado



# Funcion para devolver los Ultimos Tag Creados (+nuevos)
def get_latest_tags(
    db: Session,
    limit:int =12
):
    
    # Buscamos los ultimos main_concept Creados
    results=(
        db.query(
            Answer.main_concept.label("name")
        )
        .filter(Answer.main_concept.isnot(None)) # No Respuestas sin Tags
        .order_by(Answer.created_at.desc()) # Ordenamos de Mayor a Menor
        .limit(limit)
        .all()
    )
    
    # solo sacamos los nombres y Set para evitar que el mismo tag salga mas veeces
    unique_tags=[]
    seen_tags=set()
    
    for row in results:
        if row.name not in seen_tags:
            unique_tags.append(row.name)
            seen_tags.add(row.name)
    
    return unique_tags