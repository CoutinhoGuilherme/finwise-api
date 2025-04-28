from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .models import user, transaction
from .routers import auth, users, transactions

# Criar as tabelas no banco de dados
user.Base.metadata.create_all(bind=engine)
transaction.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial API", description="API for managing financial transactions")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Definir os domínios permitidos em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Financial API"}