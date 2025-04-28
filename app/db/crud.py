# crud.py
from sqlalchemy.orm import Session
from app import models, schemas
import uuid

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(
        id=str(uuid.uuid4()),
        title=transaction.title,
        amount=transaction.amount,
        date=transaction.date,
        category=transaction.category,
        is_recurring=transaction.is_recurring,
        recurring_type=transaction.recurring_type,
        recurring_end_date=transaction.recurring_end_date
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transaction(db: Session, transaction_id: str):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def get_transactions(db: Session):
    return db.query(models.Transaction).all()

def update_transaction(db: Session, transaction_id: str, transaction: schemas.TransactionCreate):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction:
        db_transaction.title = transaction.title
        db_transaction.amount = transaction.amount
        db_transaction.date = transaction.date
        db_transaction.category = transaction.category
        db_transaction.is_recurring = transaction.is_recurring
        db_transaction.recurring_type = transaction.recurring_type
        db_transaction.recurring_end_date = transaction.recurring_end_date
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: str):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction
