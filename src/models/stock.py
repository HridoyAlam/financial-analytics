from asset import Asset
import datetime as dt

class Stock(Asset):
    def __init__(self, 
                 ticker: str, 
                 name: str, 
                 prices: list[tuple[dt.datetime, float]], 
                 sector: str,
                 annual_dividend: float) -> None:
        super().__init__(ticker, name, prices)

        if annual_dividend < 0:
            raise ValueError("annual_dividend cannot be negative")

        self._sector = sector
        self._annual_dividend = annual_dividend

    @property
    def sector(self) -> str:
        return self._sector

    @property
    def annual_dividend(self) -> float:
        return self._annual_dividend

    def __str__(self) -> str:
        return super().__str__() + f" ({self.sector})"

    """
    Annual dividend = $2.00
    Current price   = $110
    Dividend yield = 2 / 110 × 100%
                ≈ 1.82%
    """

    def dividend_yield(self) -> float:
        return self.annual_dividend / self.current_price() * 100

    def income(self) -> float:
        return self.annual_dividend


prices = [
    (dt.datetime(2026, 1, 1), 100),
    (dt.datetime(2026, 1, 2), 105),
    (dt.datetime(2026, 1, 3), 110),
]

# apple = Stock(
#     "AAPL",
#     "Apple Inc.",
#     prices,
#     "Technology",
#     2.0
# )

# print(apple.ticker)
# print(apple.name)
# print(apple.current_price())
# print(apple.sector)
# print(apple)
# print(apple.dividend_yield())
# print(apple.income())