""" 

Schemas para Preguntas

"""

# app/schemas/question.py
from pydantic import BaseModel
from datetime import datetime

#  propiedades básicas que siempre tendrá una pregunta
class QuestionBase(BaseModel):
    title: str
    body: str # coincide con el modelo y el editor de React

#  Lo que React  envía al crear una pregunta nueva
class QuestionCreate(QuestionBase):
    # creado como buena practica, y para hacer legible el endPoint 
    # Solo pedimos título y cuerpo. 
    # El 'author_id' NO se pide aquí por seguridad, lo sacamos del token de login.
    pass 

#  devolvemos a React para mostrar
class QuestionResponse(QuestionBase):
    id: int
    views: int
    created_at: datetime
    author_id: int # Para saber quién es el dueño y dejarle puntuar las respuestas

    class Config:
        from_attributes = True