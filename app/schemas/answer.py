"""

Schemas para Respuestas

"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Any, Dict,List


# propiedades publicas del usuario (a devolver cuando se consulta una respuesta suya)
class AuthorBasicInfo(BaseModel):
    id: int
    username: str
    avatar_url: Optional[str] = None
    is_admin: bool = False

# Modelo basico
class AnswerBase(BaseModel):
    # Le decimos: "body será una lista que contiene diccionarios"
    body:List[Dict[str, Any]] # Para el JSON de la respuesta
    main_concept: Optional[str] = Field(default=None, max_length=60)


# Lo que el usuario envía desde el formulario de React
class AnswerCreate(AnswerBase):
   pass


# Lo que enviamos a React para mostrar la pantalla
class AnswerResponse(AnswerBase):
    id: int
    rating: Optional[int] = 0
    created_at: datetime
    author_id: int
    question_id: int
    author: AuthorBasicInfo

    # Configuración de Pydantic para manejar los campos como atributos directamente
    model_config= ConfigDict(from_attributes = True)

# Lo que enviamos y comprobamos al actualizar una pregunta
class AnswerUpdate(AnswerBase):
    body: Optional[Dict[str, Any]] = None
    main_concept: Optional[str] = Field(default=None, max_length=60)


# Configuracion para recibir una Votacion de una Respuesta
class AnswerVote(BaseModel):
    score: int = Field(
        ..., ge=-1, le=4, description="Puntuacion 1-4 (muy poco,poco, util, muy util)"
    )
