from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas

def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(db: Session):
    return db.query(models.Expense).order_by(models.Expense.id.desc()).all()


def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()


def delete_expense(db: Session, expense_id: int):
    expense = get_expense(db, expense_id)
    if expense:
        db.delete(expense)
        db.commit()
    return expense


def get_total_amount(db: Session):
    total = db.query(func.sum(models.Expense.amount)).scalar()
    return total or 0.0

