from pydantic import BaseModel, EmailStr, Field, ConfigDict
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
    is_admin: bool = False
    
    model_config= ConfigDict(from_attributes = True)

class UserUpdate(BaseModel):
    username: Optional[str]= None
    full_name: Optional[str]= None
    avatar_url: Optional[str]= None

class UserLeaderboard(BaseModel):
    username: str
    avatar_url: Optional[str]= None
    reputation: int
    id: int
    created_at: datetime

    model_config= ConfigDict(from_attributes = True)

class UserStats(BaseModel):
    questions_count: int
    answers_count: int
    reputation: int