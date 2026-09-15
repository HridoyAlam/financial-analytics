from stock import Stock
from position import Position
from portfolio import Portfolio
from transaction import Transaction
from cash_flow import CashFlow
from bond import Bond
from etf import ETF
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
def msft_price_history():
    return [
    (dt.datetime(2026, 1, 1), 200),
    (dt.datetime(2026, 1, 2), 205),
    (dt.datetime(2026, 1, 3), 210),
]

@pytest.fixture
def spy_price_history():
    return [
    (dt.datetime(2026, 1, 1), 500),
    (dt.datetime(2026, 1, 2), 510),
    (dt.datetime(2026, 1, 3), 520),
]

@pytest.fixture
def us10y_price_history():
    return [
    (dt.datetime(2026, 1, 1), 98),
    (dt.datetime(2026, 1, 2), 99),
    (dt.datetime(2026, 1, 3), 100),
]
@pytest.fixture
def apple_asset(apple_price_history):
    return Stock(
        "AAPL",
        "Apple Inc.",
        apple_price_history,
        "Technology",
        2.0
    )

@pytest.fixture
def msft_asset(msft_price_history):
    return Stock(
        "MSFT",
        "Microsoft Corp.",
        msft_price_history,
        "Technology",
        2.0
    )

@pytest.fixture
def position(apple_asset):
    return Position(
            apple_asset,
            quantity=100,
            average_cost=200
    )
@pytest.fixture
def portfolio():
    return Portfolio(
            "My Portfolio",
            30000,
            dt.datetime(2026, 1, 1)
        )


def test_portfolio_creation(portfolio):
    assert portfolio.name == "My Portfolio"
    assert portfolio.initial_capital == 30000
    assert portfolio.positions == {}
    assert portfolio.inception_timestamp == dt.datetime(2026,1,1)

@pytest.mark.parametrize("name", ["", " "])
def test_invalid_portfolio_name(name):
    with pytest.raises(
        ValueError,
        match="Name can't be empty"
    ):
        Portfolio(
            name,
            20000,
            dt.datetime(2026, 1, 1)
        )

@pytest.mark.parametrize("initial_capital", [0, -100])
def test_invalid_initial_capital(initial_capital):
    with pytest.raises(
        ValueError,
        match="initial_capital must be greater than zero"
    ):
        Portfolio(
            "My Portfolio",
            initial_capital,
            dt.datetime(2026, 1, 1)
        )
def test_invalid_datetime():
    with pytest.raises(
        ValueError,
        match="inception_timestamp must be a datetime"
    ):
        Portfolio(
            "My Portfolio",
            30000,
            (2026, 1, 1)
        )

def test_add_position(portfolio,apple_asset, position):
    portfolio.add_position(position)

    assert portfolio.positions[apple_asset] == position

def test_add_duplicate_asset(portfolio,apple_asset, position):
    portfolio.add_position(position)

    duplicate_position = Position(
        apple_asset,
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

# """
# Market Value = 100 × 110 = 11,000
# Cost Basis   = 100 × 200 = 20,000

# P&L = 11,000 - 20,000
#     = -9,000
# """
def test_total_pnl(portfolio, position):
    portfolio.add_position(position)
    
    value = portfolio.total_pnl()
    assert  value == -9000

# """
# P&L        = -9,000
# Total cost = 20,000

# Return = -9,000 / 20,000
#        = -0.45   
# """
# total return
 
def test_total_return(portfolio, position):
    portfolio.add_position(position)
    
    value = portfolio.total_return()
    assert  value == pytest.approx(-0.45)

def test_total_return_empty_portfolio(portfolio):

    value = portfolio.total_return()
    assert  value == 0.0
# after inception timestamp
def test_inception_timestamp(position, portfolio):
    portfolio.add_position(position)
    assert position.quantity_history == [(portfolio.inception_timestamp, 100)]
# total income

def test_total_income_empty_portfolio(portfolio):

    value = portfolio.total_income()
    assert  value == 0.0

def test_total_income(portfolio, position, spy_price_history, us10y_price_history):

    sp500 = ETF(
                "SPY",
                "SPDR S&P 500 ETF",
                spy_price_history,
                0.0945,
                7.00
            )

    bond  = Bond(
            "US10Y",
            "US Treasury 10-Year Bond",
            us10y_price_history,
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
# allocation
def test_allocation(portfolio, apple_asset, position):
    portfolio.add_position(position)
    value = portfolio.allocation(apple_asset)

    assert value == pytest.approx(20000 / 30000 *100)

def test_allocation_asset_not_found(portfolio, apple_asset):
    with pytest.raises(
        ValueError,
        match= "Asset not found in portfolio"
    ):
        portfolio.allocation(apple_asset)

# available cash

def test_available_cash(portfolio, position):
    portfolio.add_position(position)
    assert portfolio.available_cash() == pytest.approx(10000.0)

def test_available_cash_empty_portfolio( portfolio):
    assert portfolio.available_cash() == portfolio.initial_capital

# Positions

def test_remove_position(portfolio, apple_asset, position):
    portfolio.add_position(position)
    portfolio.remove_position(apple_asset)
    assert portfolio.positions == {}

def test_remove_position_asset_not_found(portfolio, apple_asset):
    with pytest.raises(
        ValueError,
        match= "Asset not found in portfolio"
        ):
            portfolio.remove_position(apple_asset)
    

def test_available_cash_after_remove(portfolio, apple_asset, position):
    portfolio.add_position(position)

    portfolio.remove_position(apple_asset)

    assert portfolio.available_cash() == pytest.approx(10000.0)

def test_position_weight(portfolio, position, apple_asset):
    portfolio.add_position(position)
    assert portfolio.position_weight(apple_asset) == pytest.approx(100.0)

def test_position_weight_asset_not_found(portfolio, apple_asset):
    with pytest.raises(
        ValueError,
        match= "Asset not found in portfolio"
        ):
        portfolio.position_weight(apple_asset)


@pytest.fixture
def sp500(spy_price_history):
    return ETF(
        "SPY",
        "SPDR S&P 500 ETF",
        spy_price_history,
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
def test_position_weight_multiple_positions(sp_position, portfolio, position, apple_asset):
    
    portfolio.add_position(position)       # 20,000
    portfolio.add_position(sp_position)   # 5,000
    # appl + spy cost = 20,000 + 5000 = 25,000 
    # appl weight = 20,000/25,000 * 100 = 80%
    assert portfolio.position_weight(apple_asset) == pytest.approx(80.0)

# apply transaction

@pytest.fixture
def buy_transaction(apple_asset):
    return Transaction(
        apple_asset,
        "BUY",
        50,
        180,
        (dt.datetime(2026, 1, 4))
    )
@pytest.fixture
def sell_transaction(apple_asset):
    return Transaction(
        apple_asset,
        "SEll",
        50,
        220,
        (dt.datetime(2026, 1, 4))
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

def test_portfolio_apply_transaction_sell_more(apple_asset, position, portfolio):
    transaction = Transaction(
        apple_asset,
        "SEll",
        110,
        220,
        (dt.datetime(2026, 1, 4))
    )
    portfolio.add_position(position)

    with pytest.raises(
            ValueError,
            match="Selling quantity cannot exceed position quantity"
        ):
        portfolio.apply_transaction(transaction)

    

def test_portfolio_apply_transaction_invalid_asset(msft_asset, portfolio):
    transaction = Transaction(msft_asset, 
                              "BUY", 50, 220,(dt.datetime(2026, 1, 4)))
    with pytest.raises(
        ValueError,
        match="Asset not found in portfolio"
    ):
     
        portfolio.apply_transaction(transaction)

def test_portfolio_apply_transaction_insufficient_cash(
        apple_asset, 
        portfolio,
        position):
    
    portfolio.add_position(position)
    transaction = Transaction(
                    apple_asset, 
                    "BUY",
                    100,
                    220,
                    (dt.datetime(2026, 1, 4)))
    with pytest.raises(
        ValueError,
        match="insufficient cash"
    ):
     
        portfolio.apply_transaction(transaction)

def test_portfolio_apply_transaction_insufficient_cash_check_old(
        apple_asset, 
        portfolio,
        position):
    
    portfolio.add_position(position)

    old_quantity = position.quantity
    old_average_cost = position.average_cost
    old_cash = portfolio.cash

    transaction = Transaction(apple_asset, "BUY", 100, 220, 
                              (dt.datetime(2026, 1, 4)))
    with pytest.raises(
        ValueError,
        match="insufficient cash"
    ):
     
        portfolio.apply_transaction(transaction)
        
    assert position.quantity == old_quantity
    assert position.average_cost == old_average_cost
    assert portfolio.cash == old_cash
def test_portfolio_apply_transaction_insufficient_cash_check_old_new(
        apple_asset, 
        portfolio,
        position):
    
    portfolio.add_position(position)

    old_quantity = position.quantity
    old_average_cost = position.average_cost
    old_cash = portfolio.cash

    print(f"old_quantity:{old_quantity}")
    print(f"old_average_cost:{old_average_cost}")
    print(f"old_cash:{old_cash}")

    transaction = Transaction(apple_asset, 
                              "BUY", 10, 220, (dt.datetime(2026, 1, 4)))
     
    portfolio.apply_transaction(transaction)

    new_quantity = position.quantity
    new_average_cost = position.average_cost
    new_cash = portfolio.cash

    print(f"new_quantity:{new_quantity}")
    print(f"new_average_cost:{new_average_cost}")
    print(f"new_cash:{new_cash}")
def test_portfolio_apply_transaction_len_check(
        apple_asset, 
        portfolio,
        position):
    
    portfolio.add_position(position)

   
    transaction = Transaction(apple_asset, "BUY", 10, 220, (dt.datetime(2026, 1, 4)))
     
    portfolio.apply_transaction(transaction)

    assert len(portfolio.transactions) == 1
def test_transactions_returns_copy(
        apple_asset,
        portfolio,
        position):

    portfolio.add_position(position)

    transaction = Transaction(apple_asset, "BUY", 10, 220, (dt.datetime(2026, 1, 4)))
    portfolio.apply_transaction(transaction)

    transactions = portfolio.transactions
    transactions.clear()

    assert len(portfolio.transactions) == 1    
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
def asset_sell(apple_asset):
    return Transaction(
            apple_asset,
            "SEll",
            100,
            220,
            (dt.datetime(2026, 1, 4))
        )

@pytest.fixture
def sp500_sell(sp500):
    return Transaction(
            sp500,
            "SEll",
            10,
            500,
            (dt.datetime(2026, 1, 4))
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
            450,
            (dt.datetime(2026, 1, 4))
        )

    portfolio.apply_transaction(sell_transaction) 
    portfolio.apply_transaction(sp500_sell)

    assert portfolio.realized_pnl() == 750


def test_realized_pnl_closed_position(portfolio, position, asset_sell):
    portfolio.add_position(position)       
    portfolio.apply_transaction(asset_sell)

    assert position.is_active is False
    assert portfolio.realized_pnl() == 2000

def test_combined_pnl(portfolio, position, sell_transaction):
    portfolio.add_position(position)
    portfolio.apply_transaction(sell_transaction)

    assert portfolio.combined_pnl() == -3500

# cash flow

@pytest.fixture
def cash_withdraw():
    return CashFlow(
            5000,
        "WITHDRAWal",
        dt.datetime(2026, 1, 1)

    )
@pytest.fixture
def cash_deposit():
    return CashFlow(
        5000,
        "DEPOSIT",
        dt.datetime(2026, 1, 1)

    )
@pytest.fixture
def large_withdrawal():
    return CashFlow(
        15000,
        "WITHDRAWal",
            dt.datetime(2026, 1, 1, 1)
    )
def test_apply_cash_flow_withdrawal(position, portfolio, cash_withdraw):
    portfolio.add_position(position)  
    portfolio.apply_cash_flow(cash_withdraw)

    assert portfolio.cash == 5000


def test_apply_cash_flow_deposit(position, portfolio, cash_deposit):

    portfolio.add_position(position)  
    portfolio.apply_cash_flow(cash_deposit)

    assert portfolio.cash == 15000

def test_apply_cash_flow_insufficient_cash(position, portfolio, large_withdrawal):
    portfolio.add_position(position)  
    
    with pytest.raises(
        ValueError,
        match="Withdrawal exceeding available cash"
    ):
        portfolio.apply_cash_flow(large_withdrawal)
        
def test_failed_withdrawal_does_not_modify_cash(position, portfolio, large_withdrawal):
    portfolio.add_position(position)  
    initial_cash = portfolio.cash
    
    with pytest.raises(
        ValueError,
        match="Withdrawal exceeding available cash"
    ):
        portfolio.apply_cash_flow(large_withdrawal)
    assert portfolio.cash == initial_cash

def test_cash_flow_is_recorded(portfolio, cash_deposit):
    portfolio.apply_cash_flow(cash_deposit)

    assert len(portfolio.cash_flows) == 1
    assert portfolio.cash_flows[0] == cash_deposit

def test_cash_flows_returns_copy(portfolio, cash_deposit):
    portfolio.apply_cash_flow(cash_deposit)

    flows = portfolio.cash_flows
    flows.clear()

    assert len(portfolio.cash_flows) == 1

# after apply cash updated with chronological order
def test_cash_flow_must_be_chronological(portfolio, cash_deposit):
    portfolio.apply_cash_flow(cash_deposit)

    cash_deposit_prev = CashFlow(
        500,
        "DEPOSIT",
        dt.datetime(2025, 1, 5)
    )
    with pytest.raises(
        ValueError,
        match= "Cash flow timestamp must be later than the previous cash flow"
    ):
        portfolio.apply_cash_flow(cash_deposit_prev)

def test_cash_flow_cannot_have_same_timestamp(portfolio, cash_deposit):
    portfolio.apply_cash_flow(cash_deposit)

    cash_withdraw = CashFlow(
            500,
            "WITHDRAWAL",
            dt.datetime(2026, 1, 1)
        )
    with pytest.raises(
            ValueError,
            match= "Cash flow timestamp must be later than the previous cash flow"
        ):
            portfolio.apply_cash_flow(cash_withdraw)

def test_cash_flow_but_have_timestamp_one_min(portfolio, cash_deposit):
    portfolio.apply_cash_flow(cash_deposit)

    cash_withdraw = CashFlow(
            500,
            "WITHDRAWAL",
            dt.datetime(2026, 1, 1, 1)
        )

    portfolio.apply_cash_flow(cash_withdraw)

    assert portfolio.cash == 34500

# # after timestamp value_at

def test_value_at_with_exact_timestamp(position, portfolio):
    portfolio.add_position(position)
    timestamp = dt.datetime(2026, 1, 3)

    assert portfolio.value_at(timestamp) == 21000

def test_value_at_timestamp_between_prices(position, portfolio):
    portfolio.add_position(position)
    timestamp = dt.datetime(2026, 1, 2, 12)

    assert portfolio.value_at(timestamp) == 10500 + portfolio.cash

def test_value_at_after_last_price(position, portfolio):
    portfolio.add_position(position)
    timestamp = dt.datetime(2026, 1, 4)

    assert portfolio.value_at(timestamp) == 21000

def test_value_at_invalid_timestamp(position, portfolio):
    portfolio.add_position(position)
    with pytest.raises(
        TypeError,
        match= "timestamp must be a datetime"
    ):
        portfolio.value_at((2026, 1, 3))

def test_value_at_before_first_price(position, portfolio):
    portfolio.add_position(position)
    timestamp = dt.datetime(2025, 12, 31)

    with pytest.raises(
        ValueError,
        match=f"No price found for timestamp {timestamp}"
    ):
        portfolio.value_at(timestamp)

def test_value_at_with_multiple_positions(position, sp_position, portfolio):
    portfolio.add_position(position)
    portfolio.add_position(sp_position)
    timestamp = dt.datetime(2026, 1, 3)
    # print("cash:", portfolio.cash)
    # print("position value:", position.value_at(timestamp))
    # print("sp value:", sp_position.value_at(timestamp))

    assert portfolio.value_at(timestamp) == (
    11000 + 5200 + portfolio.cash)

def test_value_at_includes_cash(position, portfolio):
    portfolio.add_position(position)

    timestamp = dt.datetime(2026, 1, 3)

    assert portfolio.value_at(timestamp) == 11000 + portfolio.cash

def test_value_at_historical_scenario(position, portfolio, apple_asset):
    portfolio.add_position(position)

    assert position.quantity == 100
    assert position.average_cost == 200
    assert portfolio.cash == 10000

    jan_2 = dt.datetime(2026, 1, 2)
    jan_4 = dt.datetime(2026, 1, 4)
    buy = Transaction(
        apple_asset,
        "BUY",
        10,
        210,
        jan_2
    )
    portfolio.apply_transaction(buy)
    assert portfolio.cash == 7900
    sell = Transaction(
            apple_asset,
            "SELL",
            20,
            220,
            jan_4
        )
    portfolio.apply_transaction(sell)

    
    assert portfolio.value_at(dt.datetime(2026, 1, 3)) == 17800
    assert portfolio.value_at(dt.datetime(2026, 1, 4)) == 22200
    assert portfolio.value_at(dt.datetime(2026, 1, 5)) == 22200

def test_value_at_between_transactions(position, portfolio, apple_asset):

    jan_2 = dt.datetime(2026, 1, 2)
    jan_3 = dt.datetime(2026, 1, 3)
    portfolio.add_position(position)
    buy = Transaction(
        apple_asset,
        "BUY",
        10,
        210,
        jan_2
    )
    portfolio.apply_transaction(buy)
    price_on_jan_3 = apple_asset.price_at(jan_3)
    assert position.value_at(jan_3) == 110 * price_on_jan_3

def test_value_at_after_sell(position, portfolio, apple_asset):

    jan_2 = dt.datetime(2026, 1, 2)
    jan_4 = dt.datetime(2026, 1, 4)
    jan_5 = dt.datetime(2026, 1, 5)

    portfolio.add_position(position)

    buy = Transaction(
        apple_asset,
        "BUY",
        10,
        110,
        jan_2
    )
    sell = Transaction(
        apple_asset,
        "SELL",
        20,
        90,
        jan_4
    )
    portfolio.apply_transaction(buy)
    portfolio.apply_transaction(sell)
    price_on_jan_5 = apple_asset.price_at(jan_5)
    assert position.value_at(jan_5) == 90 * price_on_jan_5




###### cash_at
def test_cash_at_with_exact_timestamp(position, portfolio):
    portfolio.add_position(position)
    timestamp = dt.datetime(2026, 1, 1)

    assert portfolio.cash_at(timestamp) == 10000

def test_cash_at_timestamp_between_prices(
        position, 
        portfolio, 
        cash_deposit, 
        large_withdrawal):
    portfolio.add_position(position)
    portfolio.apply_cash_flow(cash_deposit)
    portfolio.apply_cash_flow(large_withdrawal)
    timestamp = dt.datetime(2026, 1, 4)

    assert portfolio.cash_at(timestamp) == 0

def test_cash_at_with_different_timestamp(position, portfolio, apple_asset):
    jan_1 = dt.datetime(2026, 1, 1)
    jan_2 = dt.datetime(2026, 1, 2)
    jan_4 = dt.datetime(2026, 1, 4)
    jan_5 = dt.datetime(2026, 1, 5)
    jan_6 = dt.datetime(2026, 1, 6)
    jan_7 = dt.datetime(2026, 1, 7)
    jan_8 = dt.datetime(2026, 1, 8)

    portfolio.add_position(position)

    buy = Transaction(
        apple_asset,
        "BUY",
        10,
        200,
        jan_2
    )
    portfolio.apply_transaction(buy)

    deposit = CashFlow(
        5000,
        "DEPOSIT",
        jan_5
    )
    portfolio.apply_cash_flow(deposit)

    sell = Transaction(
        apple_asset,
        "SELL",
        15,
        200,
        jan_7
    )
    portfolio.apply_transaction(sell)

    assert portfolio.cash_at(jan_1) == 10000
    assert portfolio.cash_at(jan_2) == 8000
    assert portfolio.cash_at(jan_4) == 8000
    assert portfolio.cash_at(jan_5) == 13000
    assert portfolio.cash_at(jan_6) == 13000
    assert portfolio.cash_at(jan_8) == 16000
    