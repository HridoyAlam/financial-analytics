from abc import ABC, abstractmethod
import datetime as dt
class Asset(ABC):
    def __init__(
            self, 
            ticker: str, 
            name: str, 
            prices: list[tuple[dt.datetime, float]]
            ):

        if not ticker or not ticker.strip():
            raise ValueError("Ticker can't be empty")

        if not name or not name.strip():
            raise ValueError("Name can't be empty")

        self._validate_price_history(prices)
        
        self._ticker = ticker
        self._name = name
        self._prices = list(prices)

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def name(self) -> str:
        return self._name

    @property
    def prices(self) -> list[tuple[dt.datetime, float]]:
        return self._prices.copy()
    

    def _validate_price_history(self, prices) -> None:
        if not prices:
            raise ValueError("Prices can't be empty")

        previous_timestamp = None

        for timestamp, price in prices:

            if not isinstance(timestamp, dt.datetime):
                raise TypeError("timestamp must be a datetime")

            if previous_timestamp is not None:
                if timestamp <= previous_timestamp:
                    raise ValueError(
                        "Price history timestamps must be in strictly increasing order"
                        )
            
            if not isinstance(price, (int, float)):
                raise TypeError("price must be a number")

            if price <= 0 :
                raise ValueError("Price must be greater than 0")

            previous_timestamp = timestamp
            

        

    def __str__(self) -> str:
        return (f"{self.ticker} - {self.name}")

    def current_price(self) -> float:
        return self._prices[-1][1]

    def total_return(self) -> float:
        start_price = self._prices[0][1]
        end_price = self._prices[-1][1]

        return (end_price  /start_price) - 1
    
    def total_return_percent(self) -> float:
        return self.total_return() * 100

    # Since every type of asset in your project is supposed to provide income, 
    # income() belongs in the Asset interface.
    @abstractmethod
    def income(self) -> float:
        raise NotImplementedError





class ETF(Asset):
    pass

class Bond(Asset):
    pass

# error will show cause we change the class into abstract class
# apple = Asset(
#     "AAPL",
#     "Apple Inc.",
#     [100, 105, 110]
# )

# # print(apple.ticker)
# # print(apple.name)
# # print(apple.prices)

# # prices = apple.prices

# # prices.append(9999)

# print(apple.total_return())