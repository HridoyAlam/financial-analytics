from asset import Asset
from position import Position
from portfolio import Portfolio
import pytest
@pytest.fixture
def asset():
    return Asset(
            "AAPL",
            "Apple Inc.",
            [100, 105, 110]
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
            20000
        )


def test_portfolio_creation(portfolio):
    assert portfolio.name == "My Portfolio"
    assert portfolio.initial_capital == 20000
    assert portfolio.positions == {}

@pytest.mark.parametrize("name", ["", " "])
def test_invalid_portfolio_name(name):
    with pytest.raises(
        ValueError,
        match="Name can't be empty"
    ):
        Portfolio(
            name,
            20000
        )

@pytest.mark.parametrize("initial_capital", [0, -100])
def test_invalid_initial_capital(initial_capital):
    with pytest.raises(
        ValueError,
        match="initial_capital must be greater than zero"
    ):
        Portfolio(
            "My Portfolio",
            initial_capital
        )

def test_add_position(portfolio,asset, position):
    portfolio.add_position(position)

    assert portfolio.positions[asset] == position

def test_add_duplicate_asset(portfolio,asset, position):
    portfolio.add_position(position)

    duplicate_position = Position(
        asset,
        quantity=50,
        average_cost=105
    )

    with pytest.raises(
        ValueError,
        match="Asset already exists in portfolio"
    ):
        portfolio.add_position(duplicate_position)

def test_add_position_insufficient_capital(position):
    portfolio = Portfolio(
                "My Portfolio",
                initial_capital = 10000
            )
    with pytest.raises(
        ValueError,
        match="Insufficient capital"
    ):
        portfolio.add_position(position)

def test_current_value(portfolio, position):
    # Arrange
    portfolio.add_position(position)
    #Act
    value = portfolio.current_value()
    # Assert
    assert  value == 11000

def test_total_cost(portfolio, position):
    # Arrange
    portfolio.add_position(position)
    #Act
    value = portfolio.total_cost()
    # Assert
    assert  value == 20000

"""
Market Value = 100 × 110 = 11,000
Cost Basis   = 100 × 200 = 20,000

P&L = 11,000 - 20,000
    = -9,000
"""
def test_total_pnl(portfolio, position):
    portfolio.add_position(position)
    
    value = portfolio.total_pnl()
    assert  value == -9000

"""
P&L        = -9,000
Total cost = 20,000

Return = -9,000 / 20,000
       = -0.45   
"""
 
def test_total_return(portfolio, position):
    portfolio.add_position(position)
    
    value = portfolio.total_return()
    assert  value == pytest.approx(-0.45)

def test_total_return_empty_portfolio(portfolio):

    value = portfolio.total_return()
    assert  value == 0.0