import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"  # Valor padrão para testes
    JWT_SECRET: str = "test_secret"             # Valor padrão para testes
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 dia

    # class Config:
    #     env_file = ".env"  # Carrega automaticamente variáveis do .env

# Instância para ser importada nos outros arquivos
settings = Settings()