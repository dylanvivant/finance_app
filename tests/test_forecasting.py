import pytest
from datetime import datetime, timedelta
from models.user import User
from models.transaction import Transaction
from services.forecasting import ForecastingService

@pytest.fixture
def user():
    user = User(1, "testuser", "test@example.com")
    # Ajouter quelques transactions de test
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        user.add_transaction(Transaction(i, 1, 100, "Income", "Salary", date))
        user.add_transaction(Transaction(i+30, 1, -80, "Expense", "Living", date))
    return user

@pytest.fixture
def forecasting_service(user):
    return ForecastingService(user)

def test_predict_future_balance(forecasting_service):
    predicted_balance = forecasting_service.predict_future_balance(30)
    assert predicted_balance > 0
    assert isinstance(predicted_balance, float)

def test_predict_category_spending(forecasting_service):
    predicted_spending = forecasting_service.predict_category_spending("Expense", 30)
    assert predicted_spending > 0
    assert isinstance(predicted_spending, float)

def test_suggest_savings_goal(forecasting_service):
    savings_goal = forecasting_service.suggest_savings_goal()
    assert savings_goal >= 0
    assert isinstance(savings_goal, float)

def test_predict_future_balance_no_transactions(user):
    user.transactions = []  # Vider les transactions
    fs = ForecastingService(user)
    assert fs.predict_future_balance(30) == 0

def test_predict_category_spending_no_transactions(user):
    user.transactions = []  # Vider les transactions
    fs = ForecastingService(user)
    assert fs.predict_category_spending("Expense", 30) == 0

def test_suggest_savings_goal_expenses_exceed_income(user):
    user.transactions = [
        Transaction(1, 1, 1000, "Income", "Salary", datetime.now()),
        Transaction(2, 1, -1500, "Expense", "Living", datetime.now())
    ]
    fs = ForecastingService(user)
    assert fs.suggest_savings_goal() == 0