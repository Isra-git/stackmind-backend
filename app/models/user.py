from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    # Datos de acceso
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Datos de perfil para StackMind
    username = Column(String, unique=True, index=True, nullable=False) # alias obligatorio y único
    full_name = Column(String, nullable=True) # Nombre real, puede estar vacío
    avatar_url = Column(String, nullable=True) # URL de la imagen en Supabase Storage
    
    # Sistema del foro
    reputation = Column(Integer, default=0) 
    is_active = Column(Boolean, default=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())