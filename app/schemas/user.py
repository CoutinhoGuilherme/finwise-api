from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr

    @validator('name')
    def name_must_match_regex(cls, value):
        if not value.isalpha() and " " not in value:
            raise ValueError('Name must contain only letters and spaces')
        if not (3 <= len(value) <= 80):
            raise ValueError('Name must be between 3 and 80 characters')
        return value

class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_must_be_valid(cls, value):
        # Verifica o comprimento
        if not (8 <= len(value) <= 30):
            raise ValueError('Password must be between 8 and 30 characters')
        
        # Verifica se contém pelo menos 1 número
        if not re.search(r'\d', value):
            raise ValueError('Password must contain at least one number')
        
        # Verifica se contém pelo menos 1 caractere especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('Password must contain at least one special character')
        
        return value

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True