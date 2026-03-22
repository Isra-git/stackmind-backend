""" 

Schemas para Respuestas

"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Modelo basico
class AnswerBase(BaseModel):
    body: str
    main_concept: Optional[str]= Field(default=None, max_length=60)

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

    class Config:
        from_attributes = True