from asset import Asset
import datetime as dt
# from stock import Stock

class ETF(Asset):
    def __init__(self, 
                 ticker: str, 
                 name: str, 
                 prices: list[tuple[dt.datetime, float]], 
                 expense_ratio: float,
                 annual_distribution: float) -> None:
        super().__init__(ticker, name, prices)

        if expense_ratio < 0:
            raise ValueError("expense_ratio must be greater than zero")

        if annual_distribution < 0:
            raise ValueError("annual distribution can't be negative")
        
        self._expense_ratio = expense_ratio
        self._annual_distribution = annual_distribution

    @property
    def expense_ratio(self) -> float:
        return self._expense_ratio

    @property
    def annual_distribution(self) ->float:
        return self._annual_distribution

    def __str__(self) -> str:
        return super().__str__() + f"  {self.expense_ratio}"

    def income(self) -> float:
        return self.annual_distribution


# apple = Stock(
#     "AAPL",
#     "Apple Inc.",
#     [100, 105, 110],
#     "Technology",
# )

spy_price_history = [
    (dt.datetime(2026, 1, 1), 500),
    (dt.datetime(2026, 1, 2), 510),
    (dt.datetime(2026, 1, 3), 520)]

sp500 = ETF(
    "SPY",
    "SPDR S&P 500 ETF",
    spy_price_history,
    0.0945,
    7.00
)

# assets = [apple, sp500]
# print(sp500)
# for asset in assets:

#     # print(f"{asset.ticker} - {asset.current_price()}")
#     print(asset)

# print(sp500.income())