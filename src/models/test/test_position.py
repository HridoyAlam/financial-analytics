# to run this : ctrl + shift + p then : configure test > choose pytest
from stock import Stock
from position import Position
from transaction import Transaction
import pytest

@pytest.fixture
def asset():
    return Stock(
        "AAPL",
        "Apple Inc.",
        [100, 105, 110],
        "Technology",
        2.0
    )

@pytest.fixture
def other_asset():
    return Stock(
        "MSFT",
        "Microsoft Corp.",
        [200, 205, 210],
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
                220
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
                
    )

    position.apply_transaction(transaction1)
    assert position.realized_pnl == pytest.approx(400)

    transaction2 = Transaction(
                asset,
                "Sell",
                30,
                180,
                
    )
    position.apply_transaction(transaction2)
    assert position.realized_pnl == pytest.approx(-200)

    

def test_apply_transaction_invalid_asset(other_asset, position):

    transaction = Transaction(
                    other_asset,
                    "Buy",
                    50,
                    220
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
                    220
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
                    220
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
                    220
        )
    position.apply_transaction(transaction)
    assert  position.is_active is True

def test_is_active_after_full_sell(asset, position):
    transaction = Transaction(
                    asset,
                    "SELL",
                    100,
                    220
        )
    position.apply_transaction(transaction)
    assert  position.is_active is False

def test_is_active_initially_true(position):
    assert position.is_active is True