from transaction import Transaction
from stock import Stock
from position import Position
from portfolio import Portfolio
import pytest
import datetime as dt

@pytest.fixture
def price_history():
    return [
    (dt.datetime(2026, 1, 1), 100),
    (dt.datetime(2026, 1, 2), 105),
    (dt.datetime(2026, 1, 3), 110),
]
@pytest.fixture
def asset(price_history):
    return Stock(
        "AAPL",
        "Apple Inc.",
        price_history,
        "Technology",
        2.0
    )

@pytest.fixture
def position(asset):
    return Position(
            asset,
            quantity=100,
            average_cost=200
    )
@pytest.fixture
def portfolio():
    return Portfolio(
            "My Portfolio",
            30000
        )
@pytest.mark.parametrize("param", ["buy", "Buy", "BUY"])
def test_valid_buy_transaction(asset, param):
    transaction = Transaction(
                asset,
                param,
                20,
                500,
                dt.datetime(2026,1,5)
            )
    assert transaction.transaction_type == "BUY"
    assert transaction.quantity == 20
    assert transaction.price == 500
    assert transaction.timestamp == dt.datetime(2026, 1, 5)
@pytest.mark.parametrize("param", ["sell", "SELL", "Sell"])
def test_valid_sell_transaction(asset, param):
    transaction = Transaction(
                asset,
                param,
                20,
                500,
                dt.datetime(2026,1,5)
            )
    assert transaction.transaction_type == "SELL"
    

def test_invalid_quantity_buy_transaction(asset):
    with pytest.raises(
        ValueError,
        match="Quantity must be greater than zero"
    ):
        Transaction(
            asset,
            "BUY",
            -20,
            500,
            dt.datetime(2026,1,5)
        )
def test_invalid_price_sell_transaction(asset):
    with pytest.raises(
        ValueError,
        match="Price must be greater than zero"
    ):
        Transaction(
            asset,
            "sell",
            20,
            -500,
            dt.datetime(2026,1,5)
        )


def test_total_value(asset):
    transaction = Transaction(
        asset,
        "BUY",
        50,
        100,
        dt.datetime(2026,1,5)
        )

    assert transaction.total_value() == pytest.approx(5000)

def test_invalid_transaction_type(asset):
    with pytest.raises(
        ValueError,
        match= "Transaction type must either BUY or SELL"
    ):
        Transaction(
            asset,
            "Hold",
            50,
            100,
            dt.datetime(2026,1,5)
            )
    
def test_invalid_asset():
    with pytest.raises(
        TypeError,
        match="asset must be an instance of Asset"
    ):
        Transaction(
                    "MSTP",
                    "BUY",
                    50,
                    100,
                    dt.datetime(2026,1,5)
                    )
def test_invalid_timestamp(asset):
    with pytest.raises(
        TypeError,
        match="timestamp must be a datetime"
    ):
        Transaction(
                    asset,
                    "BUY",
                    50,
                    100,
                    (2026,1,5)
                    )