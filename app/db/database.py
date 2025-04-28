from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL
from app.core.config import settings  # Importa o settings corretamente


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Esta função faltava:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()