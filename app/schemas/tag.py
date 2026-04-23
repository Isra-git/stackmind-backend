""" 

    Schema par los Tags Auto-Generados por las Respuestas


"""

# app/schemas/tag.py

#  dependencias
from pydantic import BaseModel


# respuesta para las Tag generadas
class TagResponse(BaseModel):
    name: str #tag
    counter: int # cuantas veces se ha usado