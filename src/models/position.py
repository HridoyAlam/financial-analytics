from asset import Asset
from stock import Stock
from transaction import Transaction
import datetime as dt

class Position:
    def __init__(
            self, 
            asset: Asset, 
            quantity: float, 
            average_cost: float
            ):

        if not isinstance(asset, Asset):
            raise TypeError("asset must be an instance of Asset")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        
        if average_cost <= 0:
            raise ValueError("Average cost must be greater than zero")

        self._asset = asset
        self._quantity = quantity
        self._average_cost = average_cost

        self._realized_pnl = 0.0

    @property
    def asset(self) -> Asset:
        return self._asset

    @property
    def quantity(self) -> float:
        return self._quantity

    @property
    def average_cost(self) -> float:
        return self._average_cost

    @property
    def realized_pnl(self) -> float:
        return self._realized_pnl
    
    @property
    def is_active(self) -> bool:
        return self.quantity > 0

    def cost_basis(self) -> float:
        return self.quantity * self.average_cost

    def market_value(self) -> float:
        return self.quantity * self.asset.current_price()

    def unrealized_pnl(self) -> float:
        return self.market_value() - self.cost_basis()

    def income(self) -> float:
        return self.quantity * self.asset.income()

    def value_at(self, timestamp: dt.datetime) -> float:
        price = self.asset.price_at(timestamp)

        return self.quantity * price

    def apply_transaction(self, transaction: Transaction) -> None:
        if transaction.asset != self.asset:
            raise ValueError("Transaction asset must match position asset")

        if transaction.transaction_type == "BUY":

            old_cost = self.quantity * self.average_cost
            new_cost = transaction.quantity * transaction.price

            combined_cost = old_cost + new_cost
            new_quantity = self.quantity + transaction.quantity

            new_average_cost = combined_cost / new_quantity

            self._quantity = new_quantity
            self._average_cost = new_average_cost

        elif transaction.transaction_type == "SELL":

            if self.quantity < transaction.quantity:
                raise ValueError("Selling quantity cannot exceed position quantity")

            realized_pnl = (transaction.price - self.average_cost) * transaction.quantity

            self._quantity -= transaction.quantity
            self._realized_pnl += realized_pnl

       

price_history = [
    (dt.datetime(2026, 1, 1), 100),
    (dt.datetime(2026, 1, 2), 105),
    (dt.datetime(2026, 1, 3), 110),
]

apple = Stock(
    "AAPL",
    "Apple Inc.",
    price_history,
    "Technology",
    2.0
)

position = Position(
    asset=apple,
    quantity=100,
    average_cost=200
)

buy_transaction = Transaction(
    apple,
    "Buy",
    50,
    220,
    dt.datetime(2026, 1, 5)
)
sell_transaction = Transaction(
    apple,
    "Sell",
    30,
    220,
    dt.datetime(2026, 1, 6)
)


# print(position.asset)
# print(position.quantity)
# print(position.average_cost)
# print(position.cost_basis())
# print(position.market_value())
# print(position.unrealized_pnl())
# print(position.unrealized_pnl())
# print(position.income())

# position.apply_transaction(buy_transaction)
# print(position.quantity)
# print(position.average_cost)

position.apply_transaction(sell_transaction)
print(position.quantity)
print(position.average_cost)
print(position.realized_pnl)