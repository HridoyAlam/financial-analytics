# to run this : ctrl + shift + p then : configure test > choose pytest
from stock import Stock
from position import Position
from transaction import Transaction
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
def other_asset(price_history):
    return Stock(
        "MSFT",
        "Microsoft Corp.",
        price_history,
        "Technology",
        2.0
    )

@pytest.fixture
def position(asset):
    return Position( 
        asset,
        quantity=100, 
        average_cost=200,
        )

def test_position_creation(asset, position):
    
    assert position.asset == asset
    assert position.quantity == 100
    assert position.average_cost == 200

def test_cost_basis(position):
    assert position.cost_basis() == 20000

def test_realized_pnl (position):
    assert position.realized_pnl == 0


def test_market_value(position):

    assert position.market_value() == 11000
    

def test_unrealized_pnl(position):

    assert position.unrealized_pnl() == -9000

@pytest.mark.parametrize("quantity", [0, -1])
def test_position_invalid_quantity(asset, quantity):

    with pytest.raises(
        ValueError,
        match="Quantity must be greater than zero"
        ):
        Position(
            asset,
            quantity=quantity,
            average_cost=100
        )


@pytest.mark.parametrize("average_cost", [0, -1])
def test_position_invalid_average_cost(asset, average_cost):

    with pytest.raises(
        ValueError, 
        match="Average cost must be greater than zero"
        ):
        Position(
            asset,
            quantity=100,
            average_cost= average_cost
        )
def test_position_invalid_asset():

    with pytest.raises(
        TypeError, 
        match="asset must be an instance of Asset"
        ):
        Position(
            asset="AAPL",
            quantity=100,
            average_cost=100
)

def test_position_income(position):
    assert position.income() == pytest.approx(200.0)


def test_apply_transaction_buy(asset, position):
    transaction = Transaction(
                asset,
                "Buy",
                50,
                220,
                dt.datetime(2026,1,1)
    )
    position.apply_transaction(transaction)
    assert position.average_cost == pytest.approx(206.66666666666666)
    assert position.quantity == pytest.approx(150)

def test_apply_transaction_sell(asset, position):
    transaction = Transaction(
                asset,
                "Sell",
                50,
                220,
                dt.datetime(2026,1,1)
    )
    position.apply_transaction(transaction)
    assert position.quantity == pytest.approx(50)
    assert position.average_cost == pytest.approx(200)
    assert position.realized_pnl == pytest.approx(1000)
def test_apply_transaction_extra_sell(asset, position):
    transaction1 = Transaction(
                asset,
                "Sell",
                20,
                220,
                dt.datetime(2026,1,1)
    )

    position.apply_transaction(transaction1)
    assert position.realized_pnl == pytest.approx(400)

    transaction2 = Transaction(
                asset,
                "Sell",
                30,
                180,
                dt.datetime(2026,1,1)
    )
    position.apply_transaction(transaction2)
    assert position.realized_pnl == pytest.approx(-200)

    

def test_apply_transaction_invalid_asset(other_asset, position):

    transaction = Transaction(
                    other_asset,
                    "Buy",
                    50,
                    220,
                    dt.datetime(2026,1,1)
        )
    with pytest.raises(
        ValueError,
        match="Transaction asset must match position asset"
    ):
        position.apply_transaction(transaction)

def test_apply_transaction_over_sell(asset, position):

    transaction = Transaction(
                    asset,
                    "SELL",
                    150,
                    220,
                    dt.datetime(2026,1,1)
        )
    with pytest.raises(
        ValueError,
        match="Selling quantity cannot exceed position quantity"
    ):
        position.apply_transaction(transaction)
def test_apply_transaction_final_sell_edge_case(asset, position):

    transaction = Transaction(
                    asset,
                    "SELL",
                    100,
                    220,
                    dt.datetime(2026,1,1)
        )
    position.apply_transaction(transaction)
    assert  position.quantity ==  0
    assert  position.average_cost ==  200
    assert  position.realized_pnl ==  2000

def test_is_active_after_partial_sell(asset, position):
    transaction = Transaction(
                    asset,
                    "SELL",
                    30,
                    220,
                    dt.datetime(2026,1,1)
        )
    position.apply_transaction(transaction)
    assert  position.is_active is True

def test_is_active_after_full_sell(asset, position):
    transaction = Transaction(
                    asset,
                    "SELL",
                    100,
                    220,
                    dt.datetime(2026,1,1)
        )
    position.apply_transaction(transaction)
    assert  position.is_active is False

def test_is_active_initially_true(position):
    assert position.is_active is True


def test_value_at_with_exact_timestamp(position):
    timestamp = dt.datetime(2026, 1, 3)

    assert position.value_at(timestamp) == 11000

def test_value_at_timestamp_between_prices(position):
    timestamp = dt.datetime(2026, 1, 2, 12)

    assert position.value_at(timestamp) == 10500

def test_value_at_after_last_price(position):
    timestamp = dt.datetime(2026, 1, 4)

    assert position.value_at(timestamp) == 11000

def test_value_at_invalid_timestamp(position):
    with pytest.raises(
        TypeError,
        match= "timestamp must be a datetime"
    ):
        position.value_at((2026, 1, 3))

def test_value_at_before_first_price(position):
    timestamp = dt.datetime(2025, 12, 31)

    with pytest.raises(
        ValueError,
        match=f"No price found for timestamp {timestamp}"
    ):
        position.value_at(timestamp)

def test_initialize_quantity_history(position):
    timestamp = dt.datetime(2026, 1, 1)

    position.initialize_history(timestamp)

    assert position.quantity_history == [
        (timestamp, 100)
    ]

def test_quantity_history_returns_copy(position):
    timestamp = dt.datetime(2026, 1, 1)

    position.initialize_history(timestamp)

    history = position.quantity_history
    history.clear()

    assert position.quantity_history == [
        (timestamp, 100)
    ]

def test_quantity_history_after_transactions(asset, position):
    buy1 = Transaction(
                asset,
                "BUY",
                10,
                200,
                dt.datetime(2026,1,2)
    )
    buy2 = Transaction(
                asset,
                "BUY",
                15,
                200,
                dt.datetime(2026,1,3)
    )
    sell = Transaction(
                asset,
                "SELL",
                20,
                200,
                dt.datetime(2026,1,4)
    )

    position.initialize_history(dt.datetime(2026, 1, 1))

    position.apply_transaction(buy1)
    position.apply_transaction(buy2)
    position.apply_transaction(sell)

    assert position.quantity_at(dt.datetime(2026, 1, 1)) == 100

    assert position.quantity_history == [ 
                                         (dt.datetime(2026,1,1), 100),
                                         (dt.datetime(2026,1,2), 110),
                                         (dt.datetime(2026,1,3), 125),
                                         (dt.datetime(2026,1,4), 105)]
    