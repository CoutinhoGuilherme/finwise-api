from datetime import datetime
import re
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import validates
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(80), unique=True, index=True, nullable=False)
    firstName = Column(String(80), nullable=False)
    lastName = Column(String(80), nullable=False)
    password = Column(String(80), nullable=False)

    @validates("password")
    def validate_password(self, key, password):
        # Aceita letras, números e os caracteres !@#$%^&* com 8 a 80 caracteres
        pattern = r"^[a-zA-Z0-9!@#$%^&*]{8,80}$"

        if not re.match(pattern, password):
            raise ValueError("A senha deve ter entre 8 e 80 caracteres e conter apenas letras, números e !@#$%^&*.")
        
        return password

class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)
