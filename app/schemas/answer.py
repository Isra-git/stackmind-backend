""" 

Schemas para Respuestas

"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Lo que el usuario envía desde el formulario de React
class AnswerCreate(BaseModel):
    body: str

# Lo que enviamos a React para mostrar la pantalla
class AnswerResponse(BaseModel):
    id: int
    body: str
    rating: Optional[int] = None
    created_at: datetime
    author_id: int
    question_id: int

    class Config:
        from_attributes = True