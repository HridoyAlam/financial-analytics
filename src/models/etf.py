from asset import Asset
# from stock import Stock

class ETF(Asset):
    def __init__(self, ticker: str, name: str, prices: list[float], expense_ratio: float) -> None:
        super().__init__(ticker, name, prices)

        if expense_ratio < 0:
            raise ValueError("expense_ratio must be greater than zero")
        self._expense_ratio = expense_ratio

    @property
    def expense_ratio(self) -> float:
        return self._expense_ratio

    def __str__(self) -> str:
        return super().__str__() + f"  {self.expense_ratio}"


# apple = Stock(
#     "AAPL",
#     "Apple Inc.",
#     [100, 105, 110],
#     "Technology"
# )

sp500 = ETF(
    "SPY",
    "SPDR S&P 500 ETF",
    [500, 510, 520],
    0
)

# assets = [apple, sp500]
print(sp500)
# for asset in assets:

#     # print(f"{asset.ticker} - {asset.current_price()}")
#     print(asset)