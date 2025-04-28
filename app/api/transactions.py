# transactions.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.db.database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = crud.create_transaction(db=db, transaction=transaction)
    if db_transaction is None:
        raise HTTPException(status_code=400, detail="Transaction could not be created")
    return db_transaction

@router.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(transaction_id: str, db: Session = Depends(get_db)):
    db_transaction = crud.get_transaction(db=db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(db: Session = Depends(get_db)):
    db_transactions = crud.get_transactions(db)
    return db_transactions

@router.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(transaction_id: str, transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = crud.update_transaction(db, transaction_id=transaction_id, transaction=transaction)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: str, db: Session = Depends(get_db)):
    db_transaction = crud.delete_transaction(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}
