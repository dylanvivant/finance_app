import pytest
from datetime import datetime
from models.user import User
from models.transaction import Transaction
from models.budget import Budget
from models.stock import Stock

def test_user_creation():
    user = User(1, "testuser", "test@example.com")
    assert user.user_id == 1
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert isinstance(user.created_at, datetime)

def test_add_transaction():
    user = User(1, "testuser", "test@example.com")
    transaction = Transaction(1, 1, 100, "Income", "Salary")
    user.add_transaction(transaction)
    assert len(user.transactions) == 1
    assert user.transactions[0] == transaction

def test_add_budget():
    user = User(1, "testuser", "test@example.com")
    budget = Budget(1, 1, "Food", 300, datetime.now(), datetime.now())
    user.add_budget(budget)
    assert len(user.budgets) == 1
    assert user.budgets[0] == budget

def test_add_stock():
    user = User(1, "testuser", "test@example.com")
    stock = Stock(1, 1, "AAPL", "Apple Inc.", 10, 150.0)
    user.add_stock(stock)
    assert len(user.stocks) == 1
    assert user.stocks[0] == stock

def test_get_balance():
    user = User(1, "testuser", "test@example.com")
    user.add_transaction(Transaction(1, 1, 100, "Income", "Salary"))
    user.add_transaction(Transaction(2, 1, -50, "Expense", "Food"))
    assert user.get_balance() == 50

def test_str_representation():
    user = User(1, "testuser", "test@example.com")
    assert str(user) == "User(id=1, username=testuser, email=test@example.com)"