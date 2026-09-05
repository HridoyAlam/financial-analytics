from stock import Stock
import pytest
@pytest.fixture
def stock():
    return Stock(
        "AAPL",
        "Apple Inc.",
        [100, 105, 110],
        "Technology",
        2.0
)

def test_stock(stock):
    assert stock.ticker == "AAPL"
    assert stock.current_price() == 110

def test_dividend_yield(stock):
    assert stock.dividend_yield() == pytest.approx(1.818181)

@pytest.mark.parametrize("annual_dividend", [ -1, -2 ])
def test_invalid_annual_dividend(annual_dividend):
    with pytest.raises(
        ValueError,
        match="annual_dividend cannot be negative"
    ):
        Stock(
        "AAPL",
        "Apple Inc.",
        [100, 105, 110],
        "Technology",
        annual_dividend
    )