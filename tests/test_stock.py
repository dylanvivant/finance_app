import pytest
from datetime import datetime
from models.stock import Stock

def test_stock_creation():
    stock = Stock(1, 1, "AAPL", "Apple Inc.", 10, 150.0)
    assert stock.stock_id == 1
    assert stock.user_id == 1
    assert stock.symbol == "AAPL"
    assert stock.company_name == "Apple Inc."
    assert stock.quantity == 10
    assert stock.purchase_price == 150.0
    assert isinstance(stock.purchase_date, datetime)
    assert stock.current_price == 150.0

def test_update_current_price():
    stock = Stock(1, 1, "AAPL", "Apple Inc.", 10, 150.0)
    stock.update_current_price(160.0)
    assert stock.current_price == 160.0

def test_get_total_value():
    stock = Stock(1, 1, "AAPL", "Apple Inc.", 10, 150.0)
    assert stock.get_total_value() == 1500.0
    stock.update_current_price(160.0)
    assert stock.get_total_value() == 1600.0

def test_get_profit_loss():
    stock = Stock(1, 1, "AAPL", "Apple Inc.", 10, 150.0)
    assert stock.get_profit_loss() == 0
    stock.update_current_price(160.0)
    assert stock.get_profit_loss() == 100.0
    stock.update_current_price(140.0)
    assert stock.get_profit_loss() == -100.0

def test_str_representation():
    stock = Stock(1, 1, "AAPL", "Apple Inc.", 10, 150.0)
    assert str(stock) == "Apple Inc. (AAPL): 10 actions à 150.0€ (Achat: 150.0€)"