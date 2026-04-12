"""  
Modelo de datos de Preguntas

"""

# app/models/question.py 
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(255), nullable=False) # Para Slug -> Solo Adorno x Seo
    body = Column(Text, nullable=False) # Aquí entrará el Base64 o el HTML limpio
    views = Column(Integer, default=1, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Buscamos el User dueño de author_id para devolverlo al backend
    author= relationship("User")
    
    # Borrado en cascada de las Respuestas cuando se borra una Pregunta
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    
    # usamos decorador property para devovlver el numero de respuestas de cada pregunta
    @property
    def answers_count(self):
        return len(self.answers)