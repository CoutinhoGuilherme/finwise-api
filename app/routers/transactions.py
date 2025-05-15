from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import false, null, true
from sqlalchemy.orm import Session
from typing import List

from ..crud import transaction as transaction_crud
from ..schemas import Transaction, TransactionCreate, TransactionUpdate, User
from ..database import get_db
from ..utils.security import get_current_active_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/", response_model=List[Transaction], summary="Listar transações do usuário",
    description="Este endpoint retorna uma lista de transações do usuário autenticado. Você pode paginar os resultados fornecendo parâmetros de `skip` e `limit`.",
    responses={
        200: {
            "description": "Lista de transações",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "amount": 100.00,
                            "description": "Compra no supermercado",
                            "type": "expense",
                            "date": "2025-04-28T12:00:00",
                            "is_recurring": false,
                            "category": "Alimentação",
                            "end_date": null,
                            "user_id": 1,
                            "created_at": "2025-04-28T12:00:00",
                            "updated_at": null
                        }
                    ]
                }
            }
        },
        401: {
            "description": "Usuário não autenticado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        }
    })
def read_transactions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    transactions = transaction_crud.get_user_transactions(db, user_id=current_user.id, skip=skip, limit=limit)
    return transactions

@router.post("/", response_model=Transaction, summary="Criar nova transação",
    description="Este endpoint cria uma nova transação para o usuário autenticado. O usuário é automaticamente associado à transação.",
    responses={
        201: {
            "description": "Transação criada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "amount": 100.00,
                        "description": "Compra no supermercado",
                        "type": "expense",
                        "date": "2025-04-28T12:00:00",
                        "is_recurring": false,
                        "category": "Alimentação",
                        "end_date": null,
                        "user_id": 1,
                        "created_at": "2025-04-28T12:00:00",
                        "updated_at": null
                    }
                }
            }
        },
        400: {
            "description": "Erro na criação da transação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error creating transaction"
                    }
                }
            }
        }
    })
def create_transaction(
    transaction: TransactionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return transaction_crud.create_transaction(db=db, transaction=transaction, user_id=current_user.id)

@router.get("/{transaction_id}", response_model=Transaction, summary="Obter detalhes de uma transação",
    description="Este endpoint retorna os detalhes de uma transação específica do usuário autenticado. O usuário só pode acessar suas próprias transações.",
    responses={
        200: {
            "description": "Detalhes da transação",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "amount": 100.00,
                        "description": "Compra no supermercado",
                        "type": "expense",
                        "date": "2025-04-28T12:00:00",
                        "is_recurring": false,
                        "category": "Alimentação",
                        "end_date": null,
                        "user_id": 1,
                        "created_at": "2025-04-28T12:00:00",
                        "updated_at": null
                    }
                }
            }
        },
        404: {
            "description": "Transação não encontrada",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Transaction not found"
                    }
                }
            }
        },
        403: {
            "description": "Usuário não autorizado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authorized to access this transaction"
                    }
                }
            }
        }
    })
def read_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_transaction = transaction_crud.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if db_transaction.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this transaction")
    return db_transaction

@router.put("/{transaction_id}", response_model=Transaction, summary="Atualizar uma transação",
    description="Este endpoint permite a atualização de uma transação específica do usuário autenticado.",
    responses={
        200: {
            "description": "Transação atualizada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "amount": 150.00,
                        "description": "Compra no supermercado (atualizado)",
                        "type": "expense",
                        "date": "2025-04-28T12:00:00",
                        "is_recurring": true,
                        "category": "Alimentação",
                        "end_date": "2025-06-01T00:00:00",
                        "user_id": 1,
                        "created_at": "2025-04-28T12:00:00",
                        "updated_at": "2025-05-01T12:00:00"
                    }
                }
            }
        },
        404: {
            "description": "Transação não encontrada",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Transaction not found"
                    }
                }
            }
        },
        403: {
            "description": "Usuário não autorizado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authorized to update this transaction"
                    }
                }
            }
        }
    })
def update_transaction(
    transaction_id: int, 
    transaction: TransactionUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_transaction = transaction_crud.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if db_transaction.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this transaction")
    return transaction_crud.update_transaction(db=db, transaction_id=transaction_id, transaction=transaction)

@router.delete("/{transaction_id}", response_model=Transaction, summary="Excluir uma transação",
    description="Este endpoint permite excluir uma transação específica do usuário autenticado.",
    responses={
        200: {
            "description": "Transação excluída com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "amount": 100.00,
                        "description": "Compra no supermercado",
                        "type": "expense",
                        "date": "2025-04-28T12:00:00",
                        "is_recurring": false,
                        "category": "Alimentação",
                        "end_date": null,
                        "user_id": 1,
                        "created_at": "2025-04-28T12:00:00",
                        "updated_at": null
                    }
                }
            }
        },
        404: {
            "description": "Transação não encontrada",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Transaction not found"
                    }
                }
            }
        },
        403: {
            "description": "Usuário não autorizado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authorized to delete this transaction"
                    }
                }
            }
        }
    })
def delete_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_transaction = transaction_crud.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if db_transaction.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this transaction")
    return transaction_crud.delete_transaction(db=db, transaction_id=transaction_id)
