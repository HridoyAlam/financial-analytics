from stock import Stock
import pytest
import datetime as dt

@pytest.fixture
def apple_price_history():
    return [
    (dt.datetime(2026, 1, 1), 100),
    (dt.datetime(2026, 1, 2), 105),
    (dt.datetime(2026, 1, 3), 110),
]
@pytest.fixture
def stock(apple_price_history):
    return Stock(
        "AAPL",
        "Apple Inc.",
        apple_price_history,
        "Technology",
        2.0
)

def test_stock(stock):
    assert stock.ticker == "AAPL"
    assert stock.current_price() == 110

def test_dividend_yield(stock):
    assert stock.dividend_yield() == pytest.approx(1.818181)

@pytest.mark.parametrize("annual_dividend", [ -1, -2 ])
def test_invalid_annual_dividend(apple_price_history,annual_dividend):
    with pytest.raises(
        ValueError,
        match="annual_dividend cannot be negative"
    ):
        Stock(
        "AAPL",
        "Apple Inc.",
        apple_price_history,
        "Technology",
        annual_dividend
    )

def test_income(stock):
    assert stock.income() == pytest.approx(2.0)
    