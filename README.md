# Pocket-Tracker-API 

A clean and simple expense tracker API built with **FastAPI** and **SQLite**.

## Features

- Create a new expense
- Get all expenses
- Get expense by ID
- Delete an expense
- Get total expense amount
- Automatic interactive API docs with Swagger UI

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

## Project Structure
```bash
spendly-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE

-------------------------------------------------------------------------------------------------------

## Installation
bash
git clone https://github.com/your-username/spendly-api.git
cd spendly-api
python -m venv venv
Activate virtual environment
Windows
bash
venv\Scripts\activate
Linux / macOS
bash
source venv/bin/activate
Install dependencies
bash
pip install -r requirements.txt
Run the project
bash
uvicorn app.main:app --reload
The API will run at:

bash
http://127.0.0.1:8000
Swagger docs:

bash
http://127.0.0.1:8000/docs
Redoc docs:

bash
http://127.0.0.1:8000/redoc
API Endpoints
Root
GET /
Expenses
POST /expenses
GET /expenses
GET /expenses/{expense_id}
DELETE /expenses/{expense_id}
Summary
GET /expenses-summary/total
Example Request
Create Expense
POST /expenses

json
{
  "title": "Lunch",
  "amount": 15.75,
  "category": "Food",
  "date": "2026-06-28"
}
Example Response
json
{
  "id": 1,
  "title": "Lunch",
  "amount": 15.75,
  "category": "Food",
  "date": "2026-06-28"
}
Why this project?
This project demonstrates:

REST API development
Database integration
Data validation
Clean project structure
Beginner-friendly backend engineering
Future Improvements
Update expense endpoint
Category filtering
Monthly reports
Docker support
JWT authentication
Unit tests

