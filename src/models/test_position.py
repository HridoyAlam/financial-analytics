# to run this : ctrl + shift + p then : configure test > choose pytest
from asset import Asset
from position import Position
import pytest

@pytest.fixture
def asset():
    return Asset("AAPL", "Apple Inc.", [100, 105, 110])

@pytest.fixture
def position(asset):
    return Position( asset, quantity=100, average_cost=100)

def test_position_creation(asset, position):
    
    assert position.asset == asset
    assert position.quantity == 100
    assert position.average_cost == 100

def test_cost_basis(position):

    assert position.cost_basis() == 10000


def test_market_value(position):

    assert position.market_value() == 11000
    

def test_unrealized_pnl(position):

    assert position.unrealized_pnl() == 1000

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