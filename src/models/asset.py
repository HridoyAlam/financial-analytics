class Asset:
    def __init__(self, ticker, name, prices):

        if not ticker or not ticker.strip():
            raise ValueError("Ticker can't be empty")

        if not name or not name.strip():
            raise ValueError("Name can't be empty")

        self._validate_prices(prices)

        
        self._ticker = ticker
        self._name = name
        self._prices = list(prices)

    @property
    def ticker(self):
        return self._ticker

    @property
    def name(self):
        return self._name

    @property
    def prices(self):
            return self._prices.copy()
    

    def _validate_prices(self, prices):
        if not prices:
            raise ValueError("prices can't be empty")
        
        for price in prices:
            if price <= 0 :
                raise ValueError("Price must be greater than 0")

        

    def __str__(self):
        return (f"{self.ticker} - {self.name}")

    def current_price(self):
        return self._prices[-1]

    def total_return(self):
        start_price = self._prices[0]
        end_price = self._prices[-1]

        return (end_price  /start_price) - 1
    
    def total_return_percent(self):
        return self.total_return() * 100

class Stock(Asset):
    pass

class ETF(Asset):
    pass

class Bond(Asset):
    pass


apple = Asset(
    "AAPL",
    "Apple Inc.",
    [100, 105, 110]
)

print(apple.ticker)
print(apple.name)
print(apple.prices)

prices = apple.prices

prices.append(9999)

print(apple.prices)