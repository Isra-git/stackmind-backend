"""
    ENDPOINT PARA INTERACTUAR CON LA API DE GOOGLE AI
        Y REFINAR O MEJORAR EL PROMPT DEL USUARIO

"""

# app/routers/ai.py

#dependecias
from fastapi import APIRouter, Depends, status, HTTPException 
from pydantic import BaseModel
from sqlalchemy.orm import Session 

from app.core.ai import enhance_text_with_AI
from app.core.security import get_current_user 
from app.models.user import User 

# creamos el Router
router = APIRouter()

# definimos la clase de modelo para la entrada del usuario
class AIRequest(BaseModel):
    raw_text: str

# endPoint para el Refinador de Preguntas (Protegido)
@router.post("/enhance-question", status_code=status.HTTP_200_OK)
def enhance_question(
    request: AIRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        # texto a api IA
        improved_text = enhance_text_with_AI(request.raw_text)
        
        # devolvemos Json con el texto "mejorado"
        return {"enhanced_text": improved_text}
    
    except Exception as e:
        
        # Añadimos este print para ver el error real en la consola
        print(f"🔥 ERROR REAL DE GEMINI: {e}")
        
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Esta funcion no esta disponible de momento, vuelve a intentarlo"
        )
        
        