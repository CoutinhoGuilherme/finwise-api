# app/db/models.py

from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)  # <-- Adicionado o campo name
    hashed_password = Column(String, nullable=False)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    amount = Column(Integer)
    date = Column(String)
    category = Column(String)
    is_recurring = Column(Boolean, default=False)
    recurring_type = Column(String, nullable=True)
    recurring_end_date = Column(String, nullable=True)
