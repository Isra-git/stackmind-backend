"""  
Modelo de datos de Respuestas

"""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, JSON 
from sqlalchemy.sql import func
from app.core.database import Base

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text, nullable=False) # respuesta
    
    # Para la lista para el Timeline de daisyUI
    steps = Column(JSON, nullable=True) 
    
    rating = Column(Integer, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)