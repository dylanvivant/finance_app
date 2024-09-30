import pytest
from datetime import datetime
from models.transaction import Transaction

def test_transaction_creation():
    transaction = Transaction(1, 1, 100, "Income", "Salary")
    assert transaction.transaction_id == 1
    assert transaction.user_id == 1
    assert transaction.amount == 100
    assert transaction.category == "Income"
    assert transaction.description == "Salary"
    assert isinstance(transaction.date, datetime)

def test_is_expense():
    expense = Transaction(1, 1, -50, "Expense", "Food")
    assert expense.is_expense() == True
    assert expense.is_income() == False

def test_is_income():
    income = Transaction(1, 1, 100, "Income", "Salary")
    assert income.is_income() == True
    assert income.is_expense() == False

def test_str_representation():
    income = Transaction(1, 1, 100, "Income", "Salary")
    expense = Transaction(2, 1, -50, "Expense", "Food")
    assert "Revenu: 100€ - Income" in str(income)
    assert "Dépense: 50€ - Expense" in str(expense)