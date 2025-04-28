from .user import User, UserCreate, UserUpdate
from .transaction import Transaction, TransactionCreate, TransactionUpdate

# Esquema para autenticação
from pydantic import BaseModel
from typing import Optional  # Adicione esta linha

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None