"""

Funciones para guardar las preguntas, listar todas , las
mas recientes, buscar una pregunta por su id

"""

# app/crud/question.py

# dependencias
from sqlalchemy.orm import Session

# from sqlalchemy import func, or_
from sqlalchemy import text

from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionUpdate


# Funcion que crea y guarda la pregunta del usuario
def create_question(db: Session, question: QuestionCreate, user_id: int):

    # contenedor de la pregunta
    db_question = Question(title=question.title, body=question.body, author_id=user_id)

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
    )  # aqui sacamos solo lo enviado

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
    # parseamos la frase a buscar a formate de busqueda Postgr en castellano
    # search_format = func.plainto_tsquery('spanish', search_query)

    # realizamos la busqueda (en titulo +  cuerpo ) de la Pregunta
    """
        CONCEPTO DE FULL-TEXT SEARCH de PostgreSQL
        https://www.postgresql.org/docs/current/textsearch-intro.html

    or_ -> Or Logico -> En titulo o en Cuerpo
    to_tsvector -> transforma el texto a un vector de palabras
                -> eliminamos Stop Words (palabras comunes)
                -> eliminamos Accentos
                -> Reducimos Palabras a su Raiz Gramatical ¡
    op('@@') -> Operador de búsqueda Full-Text Search en PostgreSQL¡¡, .match()
             -> El vector hace Match o "Encaja con"
    ----------

    results = db.query(Question).filter(
        or_(
            func.to_tsvector('spanish', Question.title).op('@@')(search_format),
            func.to_tsvector('spanish', Question.body).op('@@')(search_format)
        )
    ).order_by(Question.created_at.desc()).offset(skip).limit(limit).all()
        -------------------- Probado NO funciona¡----------

    results = db.query(Question).filter(
        or_(
            Question.title.match(search_query, postgresql_regconfig='spanish'),
            Question.body.match(search_query, postgresql_regconfig='spanish')
        )
    ).order_by(Question.created_at.desc()).offset(skip).limit(limit).all()

    ---------------- tampoco funciona, problemas del traductor con supabase----

    """

    # consulta en Sql puro para evitar problemas con supabase PostgreSql
    # # title tiene mas peso(setweight) que body -> Une el título y el texto en un solo bloque
    sql_search = text("""
(
  setweight(to_tsvector('spanish', coalesce(title, '')), 'A')
  ||
  setweight(to_tsvector('spanish', coalesce(body, '')), 'B')
) @@ plainto_tsquery('spanish', :search_term)
""")

rank_expr = text("""
ts_rank_cd(
  setweight(to_tsvector('spanish', coalesce(title, '')), 'A')
  ||
  setweight(to_tsvector('spanish', coalesce(body, '')), 'B'),
  plainto_tsquery('spanish', :search_term)
) DESC
""")

results = (
    db.query(Question)
    .filter(sql_search)
    .params(search_term=search_query)
    .order_by(rank_expr)
    .offset(skip)
    .limit(limit)
    .all()
)

    # devolvemos los resultados de la busqueda
    return results
