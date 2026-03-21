"""  
Modelo de datos de Respuestas

"""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text, nullable=False) # respuesta
    
    # Concepto principal de la Respuesta
    main_concept = Column(Text, nullable=True)
    
    rating = Column(Integer, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)