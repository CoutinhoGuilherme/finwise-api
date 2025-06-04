from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .models import user, transaction
from .routers import auth, users, transactions

# Criar as tabelas no banco de dados
user.Base.metadata.create_all(bind=engine)
transaction.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FinWise API", description="API for managing financial transactions")

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
    return {"message": "Welcome to FinWise API"}

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=5432)
