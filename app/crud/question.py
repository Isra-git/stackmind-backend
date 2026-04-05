"""

Funciones para guardar las preguntas, listar todas , las
mas recientes, buscar una pregunta por su id

"""

# app/crud/question.py

# dependencias
from sqlalchemy.orm import Session
from sqlalchemy import text

import unicodedata
import re


from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionUpdate

# Funcion que Genera el SLUG (solo decara Url)
def slug_generator(text: str) -> str:
    # Eliminamos los acentos y caracteres especiales
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    
    # Todo a minusculas
    text= text.lower()
    
    # Eliminamos espacios y caracteres especiales (no letra o numero)
    text= re.sub(r'[^a-z0-9]+', '-', text)
    
    # Eliminamos guiones al principio y al final
    clean_text= text.strip('-')

    # devolvemos el slug formateado
    return clean_text
    
# Funcion que crea y guarda la pregunta del usuario
def create_question(db: Session, question: QuestionCreate, user_id: int):

    # generamos el Slug sobre el titulo
    slug_genered= slug_generator(question.title) # llamamos a la funcion
    
    # contenedor de la pregunta
    db_question = Question(title=question.title, slug=slug_genered,body=question.body, author_id=user_id)

    # guardamos en la bd
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    return db_question


# Funcion que lee  las preguntas: mas recientes ordenadas por create_at Desc.
def get_questions(db: Session, skip: int = 0, limit: int = 100):
    recent_question = (
        db.query(Question)
        .order_by(Question.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return recent_question


# Funcion que busca y devuelve una pregunta por el Id
def get_question(db: Session, question_id: int):
    question_by_id = db.query(Question).filter(Question.id == question_id).first()
    return question_by_id


# Funcion para Editar una Pregunta
def update_question(db: Session, db_question: Question, question_input: QuestionUpdate):

    # scamos de Json solo los datos que el usuario ha -Enviado-
    update_data = question_input.model_dump(
        exclude_unset=True
    )  # aqui sacamos solo lo que nos han enviado
    
    # si Modifica el Titulo, Modificamos el Slug
    if "title" in update_data:
        update_data["slug"]=slug_generator(update_data["title"])

    # actualizamos el objeto para la Bd campo x campo (solo los que edito)
    for key, value in update_data.items():
        setattr(db_question, key, value)

    # guardamos los cambios en Db
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


# Funcion para Eliminar una Pregunta
def delete_question(db: Session, db_question: Question):

    db.delete(db_question)
    db.commit()
    return db_question


# Funcion para Buscar Preguntas , usando [Full-Text Search ] de PostreSQL en castellano
def search_questions(db: Session, search_query: str, skip: int = 0, limit: int = 20):
   
    """
        CONCEPTO DE FULL-TEXT SEARCH de PostgreSQL
    

    or_ -> Or Logico -> En titulo o en Cuerpo
    to_tsvector -> transforma el texto a un vector de palabras
                -> eliminamos Stop Words (palabras comunes)
                -> eliminamos Accentos
                -> Reducimos Palabras a su Raiz Gramatical ¡
    op('@@') -> Operador de búsqueda Full-Text Search en PostgreSQL¡¡, .match()
             -> El vector hace Match o "Encaja con"
    ----------

    """
    # Limpiamos la entrada para evitar errores de sintaxis en PostgreSQL
    # Solo dejamos letras, números y espacios
    clean_query = re.sub(r"[^\w\s]", "", search_query).strip()

    # Si la búsqueda se queda vacía tras limpiar, devolvemos lista vacía
    if not clean_query:
        return []

    #  Convertimos "como usar preg" en "como:* & usar:* & preg:*"
    # * indica prefijo. Postgres buscará en el índice GIN lexemas que EMPIECEN por esas letras.
    tsquery_string = " & ".join([f"{word}:*" for word in clean_query.split()])

    # Consulta SQL usando to_tsquery (que soporta los comodines :*)
    sql_search = text("""
        search_vector @@ to_tsquery('spanish', :search_term)
    """)

    # Fórmula de ranking para ordenar los resultados (Título pesa más que el cuerpo)
    rank_expr = text("""
        ts_rank_cd(search_vector, to_tsquery('spanish', :search_term)) DESC
    """)

    # Ejecutamos la consulta
    results = (
        db.query(Question)
        .filter(sql_search)
        .params(search_term=tsquery_string)
        .order_by(rank_expr)
        .offset(skip)
        .limit(limit)
        .all()
    )
   
    # devolvemos la lista de  resultados de la busqueda
    return results
