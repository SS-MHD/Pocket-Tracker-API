# =========================
# file: app/__init__.py
# =========================
# empty file


# =========================
# file: app/database.py
# =========================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./spendly.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# =========================
# file: app/models.py
# =========================
from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False)


# =========================
# file: app/schemas.py
# =========================
from pydantic import BaseModel, Field
from datetime import date

class ExpenseBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=100, example="Lunch")
    amount: float = Field(..., gt=0, example=12.5)
    category: str = Field(..., min_length=2, max_length=50, example="Food")
    date: date = Field(..., example="2026-06-28")


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# file: app/crud.py
# =========================
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


# =========================
# file: app/main.py
# =========================
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal, engine, Base
from app import schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spendly API",
    description="A simple and clean expense tracker API built with FastAPI",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "Welcome to Spendly API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.post("/expenses", response_model=schemas.ExpenseResponse, status_code=201)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)


@app.get("/expenses", response_model=List[schemas.ExpenseResponse])
def read_expenses(db: Session = Depends(get_db)):
    return crud.get_expenses(db)


@app.get("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = crud.get_expense(db, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = crud.delete_expense(db, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully", "expense_id": expense_id}


@app.get("/expenses-summary/total")
def get_total(db: Session = Depends(get_db)):
    total = crud.get_total_amount(db)
    return {"total_expenses": total}
