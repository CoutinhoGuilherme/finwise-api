from sqlalchemy.orm import Session
from ..models.transaction import Transaction
from ..schemas.transaction import TransactionCreate, TransactionUpdate

def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

def get_user_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Transaction).filter(Transaction.user_id == user_id).offset(skip).limit(limit).all()

def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction(db: Session, transaction_id: int, transaction: TransactionUpdate):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        update_data = transaction.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_transaction, key, value)
        
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction