# to run this : ctrl + shift + p then : configure test > choose pytest
from asset import Asset
from position import Position
import pytest



def test_position_creation():
    asset = Asset("AAPL", "Apple Inc.", [100, 105, 110])

    position = Position(
        asset,
        quantity=100,
        average_cost=100
    )



    assert position.asset == asset
    assert position.quantity == 100
    assert position.average_cost == 100

def test_cost_basis():
    asset = Asset("AAPL", "Apple Inc.", [100, 105, 110])

    position = Position(
        asset,
        quantity=100,
        average_cost=100
    )

    assert position.cost_basis() == 10000


def test_market_value():
    asset = Asset("AAPL", "Apple Inc.", [100, 105, 110])
    
    position = Position(
            asset,
            quantity=100,
            average_cost=100
        )

    assert position.market_value() == 11000
    

def test_unrealized_pnl():
    asset = Asset("AAPL", "Apple Inc.", [100, 105, 110])
        
    position = Position(
                asset,
                quantity=100,
                average_cost=100
            )
    
    assert position.unrealized_pnl() == 1000


def test_position_invalid_quantity():
    asset = Asset("AAPL", "Apple Inc.", [100, 105, 110])

    with pytest.raises(ValueError):
        Position(
            asset,
            quantity=0,
            average_cost=100
        )

def test_position_invalid_quantity():
    asset = Asset("AAPL", "Apple Inc.", [100, 105, 110])

    with pytest.raises(
        ValueError, 
        match="Quantity must be greater than zero"
        ):
        Position(
            asset,
            quantity=0,
            average_cost=100
        )

def test_position_invalid_average_cost():
    asset = Asset("AAPL", "Apple Inc.", [100, 105, 110])

    with pytest.raises(
        ValueError, 
        match="Average cost must be greater than zero"
        ):
        Position(
            asset,
            quantity=100,
            average_cost=0
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