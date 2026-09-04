from asset import Asset

class Stock(Asset):
    def __init__(self, ticker: str, name: str, prices: list[float], sector: str) -> None:
        super().__init__(ticker, name, prices)
        self._sector = sector

    @property
    def sector(self) -> str:
        return self._sector
        

    def __str__(self) -> str:
        return super().__str__() + f" ({self.sector})"

apple = Stock(
    "AAPL",
    "Apple Inc.",
    [100, 105, 110],
    "Technology"
)

# print(apple.ticker)
# print(apple.name)
# print(apple.current_price())
# print(apple.sector)
# print(apple)