from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional #para los campos opcionales

class UserBase(BaseModel):
    email: EmailStr
    username: str # Obligatorio
    full_name: Optional[str] = None # Opcional
    avatar_url: Optional[str] = None # Opcional

class UserCreate(UserBase):
    password: str= Field(..., max_length=50) 

class UserResponse(UserBase):
    id: int
    reputation: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True