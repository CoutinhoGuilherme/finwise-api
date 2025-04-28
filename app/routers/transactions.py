from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..crud import transaction as transaction_crud
from ..schemas import Transaction, TransactionCreate, TransactionUpdate, User
from ..database import get_db
from ..utils.security import get_current_active_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/", response_model=List[Transaction])
def read_transactions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    transactions = transaction_crud.get_user_transactions(db, user_id=current_user.id, skip=skip, limit=limit)
    return transactions

@router.post("/", response_model=Transaction)
def create_transaction(
    transaction: TransactionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return transaction_crud.create_transaction(db=db, transaction=transaction, user_id=current_user.id)

@router.get("/{transaction_id}", response_model=Transaction)
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

@router.put("/{transaction_id}", response_model=Transaction)
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

@router.delete("/{transaction_id}", response_model=Transaction)
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