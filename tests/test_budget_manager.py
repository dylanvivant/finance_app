import pytest
from datetime import datetime, timedelta
from models.user import User
from models.budget import Budget
from models.transaction import Transaction
from services.budget_manager import BudgetManager

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
@pytest.fixture
def user():
    return User(1, "testuser", "test@example.com")

@pytest.fixture
def budget_manager(user):
    return BudgetManager(user)

def test_create_budget(budget_manager):
    now = datetime.now()
    budget = budget_manager.create_budget("Groceries", 300, now, now + timedelta(days=30))
    assert isinstance(budget, Budget)
    assert budget.category == "Groceries"
    assert budget.amount == 300
    assert len(budget_manager.user.budgets) == 1

def test_get_budget_by_category(budget_manager):
    now = datetime.now()
    budget_manager.create_budget("Groceries", 300, now, now + timedelta(days=30))
    budget_manager.create_budget("Entertainment", 100, now, now + timedelta(days=30))
    groceries_budgets = budget_manager.get_budget_by_category("Groceries")
    assert len(groceries_budgets) == 1
    assert groceries_budgets[0].category == "Groceries"

def test_get_budget_status(budget_manager):
    now = datetime.now()
    budget_manager.create_budget("Groceries", 300, now, now + timedelta(days=30))
    budget_manager.create_budget("Entertainment", 100, now, now + timedelta(days=30))
    budget_manager.update_budget_spent("Groceries", 50)
    status = budget_manager.get_budget_status()
    assert "Groceries" in status
    assert "Entertainment" in status
    assert status["Groceries"]["allocated"] == 300
    assert status["Groceries"]["spent"] == 50
    assert status["Groceries"]["remaining"] == 250

def test_handle_transaction_deletion(budget_manager):
    now = datetime.now()
    budget_manager.create_budget("Groceries", 300, now, now + timedelta(days=30))
    transaction = Transaction(1, 1, -50, "Groceries", "Weekly shopping", now)
    budget_manager.update_budget_spent("Groceries", -50)  # Dépense initiale de 50
    budget_manager.handle_transaction_deletion(transaction)
    groceries_budget = budget_manager.get_budget_by_category("Groceries")[0]
    assert groceries_budget.spent == 0  # La dépense a été annulée

def test_update_budget_spent(budget_manager):
    now = datetime.now()
    budget_manager.create_budget("Groceries", 300, now, now + timedelta(days=30))
    budget_manager.update_budget_spent("Groceries", -50)  # Dépense de 50
    groceries_budget = budget_manager.get_budget_by_category("Groceries")[0]
    assert abs(groceries_budget.spent) == 50

def test_handle_transaction_update(budget_manager):
    now = datetime.now()
    budget_manager.create_budget("Groceries", 300, now, now + timedelta(days=30))
    old_transaction = Transaction(1, 1, -50, "Groceries", "Weekly shopping", now)
    new_transaction = Transaction(1, 1, -75, "Groceries", "Weekly shopping + extras", now)
    budget_manager.update_budget_spent("Groceries", -50)  # Dépense initiale de 50
    budget_manager.handle_transaction_update(old_transaction, new_transaction)
    groceries_budget = budget_manager.get_budget_by_category("Groceries")[0]
    assert abs(groceries_budget.spent) == 75
