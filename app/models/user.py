from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date 
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)  # Novo campo
    last_name = Column(String(50), nullable=False)   # Novo campo
    email = Column(String(100), unique=True, index=True, nullable=False)
    birthday = Column(Date, nullable=True)           # Novo campo
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan"