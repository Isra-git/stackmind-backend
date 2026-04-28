""" 

    Schema par los Tags Auto-Generados por las Respuestas


"""

# app/schemas/tag.py

#  dependencias
from pydantic import BaseModel
from typing import Optional

# respuesta para las Tag generadas
class TagResponse(BaseModel):
    name: str #tag
    counter: Optional[int]=0 # cuantas veces se ha usado