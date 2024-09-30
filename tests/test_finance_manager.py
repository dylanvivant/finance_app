import pytest
from datetime import datetime, timedelta
from models.user import User
from models.transaction import Transaction
from services.finance_manager import FinanceManager

@pytest.fixture
def user():
    return User(1, "testuser", "test@example.com")

@pytest.fixture
def finance_manager(user):
    return FinanceManager(user)

def test_add_transaction(finance_manager):
    transaction = finance_manager.add_transaction(100, "Income", "Salary")
    assert isinstance(transaction, Transaction)
    assert transaction.amount == 100
    assert transaction.category == "Income"
    assert transaction.description == "Salary"
    assert len(finance_manager.user.transactions) == 1
    assert "Income" in finance_manager.categories

def test_get_balance(finance_manager):
    finance_manager.add_transaction(100, "Income", "Salary")
    finance_manager.add_transaction(-50, "Expense", "Groceries")
    assert finance_manager.get_balance() == 50

def test_get_transactions_by_category(finance_manager):
    finance_manager.add_transaction(100, "Income", "Salary")
    finance_manager.add_transaction(50, "Income", "Bonus")
    finance_manager.add_transaction(-50, "Expense", "Groceries")
    income_transactions = finance_manager.get_transactions_by_category("Income")
    assert len(income_transactions) == 2
    assert all(t.category == "Income" for t in income_transactions)

def test_get_total_by_category(finance_manager):
    finance_manager.add_transaction(100, "Income", "Salary")
    finance_manager.add_transaction(50, "Income", "Bonus")
    finance_manager.add_transaction(-50, "Expense", "Groceries")
    totals = finance_manager.get_total_by_category()
    assert totals["Income"] == 150
    assert totals["Expense"] == -50

def test_get_transactions_for_period(finance_manager):
    now = datetime.now()
    finance_manager.add_transaction(100, "Income", "Salary")
    finance_manager.user.transactions[0].date = now - timedelta(days=1)
    finance_manager.add_transaction(-50, "Expense", "Groceries")
    finance_manager.user.transactions[1].date = now + timedelta(days=1)
    transactions = finance_manager.get_transactions_for_period(now - timedelta(days=2), now)
    assert len(transactions) == 1
    assert transactions[0].amount == 100