from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://dbfinwise_user:ljq2WgJrTECrUlJ3os3I7cb3bkZO3J5x@dpg-d062ar2li9vc73duftr0-a.oregon-postgres.render.com/dbfinwise"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
