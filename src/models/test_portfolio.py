from stock import Stock
from position import Position
from portfolio import Portfolio
from bond import Bond
from etf import ETF
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


def test_portfolio_creation(portfolio):
    assert portfolio.name == "My Portfolio"
    assert portfolio.initial_capital == 30000
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

def test_total_income_empty_portfolio(portfolio):

    value = portfolio.total_income()
    assert  value == 0.0

def test_total_income(portfolio, position):

    sp500 = ETF(
                "SPY",
                "SPDR S&P 500 ETF",
                [500, 510, 520],
                0.0945,
                7.00
            )

    bond  = Bond(
            "US10Y",
            "US Treasury 10-Year Bond",
            [98, 99, 100],
            1000,
            4.25,
            10
        )

    sp_position = Position(
         sp500,
         quantity= 10,
         average_cost= 100
     )
    bond_position = Position(
        bond,
        quantity=20,
        average_cost=150
    )

    portfolio.add_position(sp_position)
    portfolio.add_position(bond_position)
    portfolio.add_position(position)
    assert portfolio.total_income() == pytest.approx(1120.0)

def test_allocation(portfolio, asset, position):
    portfolio.add_position(position)
    value = portfolio.allocation(asset)

    assert value == pytest.approx(20000 / 30000 *100)

def test_allocation_asset_not_found(portfolio, asset):
    with pytest.raises(
        ValueError,
        match= "Asset not found in portfolio"
    ):
        portfolio.allocation(asset)