from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    description: str 
    type: str  
    date: datetime
    is_recurring: Optional[bool] = False
    category: str
    end_date: Optional[datetime] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    type: Optional[str] = None
    date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    category: Optional[str] = None
    end_date: Optional[datetime] = None

class Transaction(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True