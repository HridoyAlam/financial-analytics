from stock import Stock
from etf import ETF
from bond import Bond
from position import Position
from portfolio import Portfolio

apple = Stock(
    "AAPL",
    "Apple Inc.",
    [100, 105, 110],
    "Technology"
)

spy = ETF(
    "SPY",
    "SPDR S&P 500 ETF",
    [500, 510, 520],
    0.0945
)

bond = Bond(
    "US10Y",
    "US Treasury 10-Year Bond",
    [98, 99, 100],
    1000,
    4.25,
    10
)

portfolio = Portfolio(
    "My Investment Portfolio",
    100000
)

assets = [apple, spy, bond]

# for asset in assets:
#     print(asset.ticker)
#     print(asset.current_price())
#     print(asset.total_return())

apple_position = Position(
    apple,
    quantity=100,
    average_cost=100
)
spy_position = Position(
    spy,
    quantity=50,
    average_cost=500
)
bond_position = Position(
    bond,
    quantity=10,
    average_cost=98
)


portfolio.add_position(apple_position)
portfolio.add_position(spy_position)
portfolio.add_position(bond_position)

print(portfolio.current_value())
print(portfolio.total_cost())
print(portfolio.total_pnl())
print(portfolio.total_return())