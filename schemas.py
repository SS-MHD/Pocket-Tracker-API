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
