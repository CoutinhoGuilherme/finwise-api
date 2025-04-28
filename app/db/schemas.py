from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    title: str
    amount: float
    date: str
    category: str
    is_recurring: Optional[bool] = False
    recurring_type: Optional[str] = None
    recurring_end_date: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: str

    class Config:
        orm_mode = True
