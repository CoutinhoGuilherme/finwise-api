from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional
from datetime import datetime, date  # Adicione date
import re

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    birthday: Optional[date] = None  # Novo campo

    # Validação para firstName
    @validator('first_name')
    def first_name_must_match_regex(cls, value):
        if not value.isalpha():
            raise ValueError('First name must contain only letters')
        if not (2 <= len(value) <= 50):
            raise ValueError('First name must be between 2 and 50 characters')
        return value

    # Validação para lastName
    @validator('last_name')
    def last_name_must_match_regex(cls, value):
        if not value.isalpha():
            raise ValueError('Last name must contain only letters')
        if not (2 <= len(value) <= 50):
            raise ValueError('Last name must be between 2 and 50 characters')
        return value
    
        @validator('birthday')
    def birthday_must_be_past(cls, value):
        if value and value > date.today():
            raise ValueError('Birthday must be in the past')
        return value


class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_must_be_valid(cls, value):
        if not (8 <= len(value) <= 30):
            raise ValueError('Password must be between 8 and 30 characters')
        if not re.search(r'\d', value):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('Password must contain at least one special character')
        return value

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    birthday: Optional[date] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True