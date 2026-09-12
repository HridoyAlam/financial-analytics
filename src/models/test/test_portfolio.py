from stock import Stock
from position import Position
from portfolio import Portfolio
from transaction import Transaction
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

def test_available_cash(portfolio, position):
    portfolio.add_position(position)
    assert portfolio.available_cash() == pytest.approx(10000.0)

def test_available_cash_empty_portfolio( portfolio):
    assert portfolio.available_cash() == portfolio.initial_capital

def test_remove_position(portfolio, asset, position):
    portfolio.add_position(position)
    portfolio.remove_position(asset)
    assert portfolio.positions == {}

def test_remove_position_asset_not_found(portfolio, asset):
    with pytest.raises(
        ValueError,
        match= "Asset not found in portfolio"
        ):
            portfolio.remove_position(asset)
    

def test_available_cash_after_remove(portfolio, asset, position):
    portfolio.add_position(position)

    portfolio.remove_position(asset)

    assert portfolio.available_cash() == pytest.approx(10000.0)

def test_position_weight(portfolio, position, asset):
    portfolio.add_position(position)
    assert portfolio.position_weight(asset) == pytest.approx(100.0)

def test_position_weight_asset_not_found(portfolio, asset):
    with pytest.raises(
        ValueError,
        match= "Asset not found in portfolio"
        ):
        portfolio.position_weight(asset)
@pytest.fixture
def sp500():
    return ETF(
        "SPY",
        "SPDR S&P 500 ETF",
        [500, 510, 520],
        0.0945,
        7.00
    )
@pytest.fixture
def sp_position(sp500):
    return Position(
            sp500,
            quantity=10,
            average_cost=500
    )
def test_position_weight_multiple_positions(sp_position, portfolio, position, asset):
    
    portfolio.add_position(position)       # 20,000
    portfolio.add_position(sp_position)   # 5,000
    # appl + spy cost = 20,000 + 5000 = 25,000 
    # appl weight = 20,000/25,000 * 100 = 80%
    assert portfolio.position_weight(asset) == pytest.approx(80.0)

@pytest.fixture
def buy_transaction(asset):
    return Transaction(
        asset,
        "BUY",
        50,
        180
    )
@pytest.fixture
def sell_transaction(asset):
    return Transaction(
        asset,
        "SEll",
        50,
        220
    )

def test_portfolio_apply_transaction(buy_transaction, position, portfolio):
    portfolio.add_position(position)
    portfolio.apply_transaction(buy_transaction)

    assert position.quantity == 150
    assert position.average_cost == pytest.approx(193.333333)

def test_portfolio_apply_transaction_sell(sell_transaction, position, portfolio):
    
    portfolio.add_position(position)
    portfolio.apply_transaction(sell_transaction)

    assert position.quantity == 50
    assert position.realized_pnl == pytest.approx(1000.0)

def test_portfolio_apply_transaction_sell_more(asset, position, portfolio):
    transaction = Transaction(
        asset,
        "SEll",
        110,
        220
    )
    portfolio.add_position(position)

    with pytest.raises(
            ValueError,
            match="Selling quantity cannot exceed position quantity"
        ):
        portfolio.apply_transaction(transaction)

    

def test_portfolio_apply_transaction_invalid_asset(other_asset, portfolio):
    transaction = Transaction(other_asset, "BUY", 50, 220)
    with pytest.raises(
        ValueError,
        match="Asset not found in portfolio"
    ):
     
        portfolio.apply_transaction(transaction)
        
def test_initial_cash(portfolio):
    assert portfolio.initial_capital == 30000

def test_buy_reduce_cash(buy_transaction, position,portfolio):
    portfolio.add_position(position)
    portfolio.apply_transaction(buy_transaction)

    assert portfolio.available_cash() == pytest.approx(1000.0)

def test_sell_increase_cash(sell_transaction, position,portfolio):
    portfolio.add_position(position)
    portfolio.apply_transaction(sell_transaction)

    assert portfolio.available_cash() == pytest.approx(21000.0)

def test_active_positions(portfolio, position, sp_position):
    portfolio.add_position(position)       
    portfolio.add_position(sp_position)   

    assert portfolio.active_positions() == [position, sp_position]

@pytest.fixture
def asset_sell(asset):
    return Transaction(
            asset,
            "SEll",
            100,
            220
        )

@pytest.fixture
def sp500_sell(sp500):
    return Transaction(
            sp500,
            "SEll",
            10,
            500
        )

def test_active_positions_excludes_closed_sp500_position(
    portfolio,
    position,
    asset_sell,
    sp_position   
):
    
    portfolio.add_position(position)       
    portfolio.add_position(sp_position) 

    portfolio.apply_transaction(asset_sell)

    assert portfolio.active_positions() == [sp_position]

def test_active_positions_excludes_closed_position_extra(
    portfolio,
    position,
    sp500_sell,
    sp_position   
):
    portfolio.add_position(position)       
    portfolio.add_position(sp_position) 

    portfolio.apply_transaction(sp500_sell)
    
    assert portfolio.active_positions() == [position]

def test_closed_positions_asset_position(
    portfolio,
    position,
    sp500_sell,
    sp_position   
):
    
    portfolio.add_position(position)       
    portfolio.add_position(sp_position) 

    portfolio.apply_transaction(sp500_sell)

    assert portfolio.closed_positions() == [sp_position]

def test_closed_positions_sp500_position(
    portfolio,
    position,
    asset_sell,
    sp_position   
):
    portfolio.add_position(position)       
    portfolio.add_position(sp_position) 

    portfolio.apply_transaction(asset_sell)

    assert portfolio.closed_positions() == [position]

def test_closed_positions_empty(portfolio, position):
    portfolio.add_position(position)

    assert portfolio.closed_positions() == []

def test_realized_pnl_multiple_positions(
        sp500, portfolio, position, sp_position ,sell_transaction):
    portfolio.add_position(position)
    portfolio.add_position(sp_position)

    sp500_sell = Transaction(
            sp500,
            "SEll",
            5,
            450
        )

    portfolio.apply_transaction(sell_transaction) 
    portfolio.apply_transaction(sp500_sell)

    assert portfolio.realized_pnl() == 750


def test_realized_pnl_closed_position(
    portfolio,
    position,
    asset_sell,
       
):
    portfolio.add_position(position)       
    portfolio.apply_transaction(asset_sell)

    assert position.is_active is False
    assert portfolio.realized_pnl() == 2000