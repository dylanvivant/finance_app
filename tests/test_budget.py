import pytest
from datetime import datetime, timedelta
from models.budget import Budget

def test_budget_creation():
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)
    budget = Budget(1, 1, "Food", 300, start_date, end_date)
    assert budget.budget_id == 1
    assert budget.user_id == 1
    assert budget.category == "Food"
    assert budget.amount == 300
    assert budget.period_start == start_date
    assert budget.period_end == end_date
    assert budget.spent == 0

def test_add_expense():
    budget = Budget(1, 1, "Food", 300, datetime.now(), datetime.now())
    budget.add_expense(50)
    assert budget.spent == 50
    budget.add_expense(30)
    assert budget.spent == 80

def test_get_remaining():
    budget = Budget(1, 1, "Food", 300, datetime.now(), datetime.now())
    budget.add_expense(50)
    assert budget.get_remaining() == 250

def test_is_overbudget():
    budget = Budget(1, 1, "Food", 300, datetime.now(), datetime.now())
    assert budget.is_overbudget() == False
    budget.add_expense(350)
    assert budget.is_overbudget() == True

def test_str_representation():
    budget = Budget(1, 1, "Food", 300, datetime.now(), datetime.now())
    budget.add_expense(50)
    assert str(budget) == "Budget pour Food: 300€ (Dépensé: 50€, Restant: 250€)"