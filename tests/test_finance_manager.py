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

def test_delete_transaction(finance_manager):
    transaction = finance_manager.add_transaction(100, "Income", "Salary")
    assert len(finance_manager.user.transactions) == 1
    deleted_transaction = finance_manager.delete_transaction(transaction.transaction_id)
    assert deleted_transaction == transaction
    assert len(finance_manager.user.transactions) == 0
    assert "Income" not in finance_manager.categories

def test_delete_nonexistent_transaction(finance_manager):
    assert finance_manager.delete_transaction(999) is None

def test_update_transaction(finance_manager):
    transaction = finance_manager.add_transaction(100, "Income", "Salary")
    updated_transaction = finance_manager.update_transaction(transaction.transaction_id, 150, "Bonus", "Year-end bonus")
    assert updated_transaction is not None
    assert updated_transaction.amount == 150
    assert updated_transaction.category == "Bonus"
    assert updated_transaction.description == "Year-end bonus"
    assert "Bonus" in finance_manager.categories
    assert "Income" not in finance_manager.categories

def test_update_nonexistent_transaction(finance_manager):
    assert finance_manager.update_transaction(999, 100, "Test", "Test") is None
