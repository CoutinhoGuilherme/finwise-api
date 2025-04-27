import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine
from app.models import User

# Cria as tabelas no banco de dados
print("Criando banco de dados...")
User.metadata.create_all(engine)
print("Banco de dados criado com sucesso.")
