from asset import Asset

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

    @property
    def asset(self) -> Asset:
        return self._asset

    @property
    def quantity(self) -> float:
        return self._quantity

    @property
    def average_cost(self) -> float:
        return self._average_cost

    def cost_basis(self) -> float:
        return self.quantity * self.average_cost

    def market_value(self) -> float:
        return self.quantity * self.asset.current_price()

    def unrealized_pnl(self) -> float:
        return self.market_value() - self.cost_basis()

# apple = Asset(
#     "AAPL",
#     "Apple Inc.",
#     [100, 105, 110]
# )

# position = Position(
#     asset=apple,
#     quantity=100,
#     average_cost=100
# )

# print(position.asset)
# print(position.quantity)
# print(position.average_cost)
# print(position.cost_basis())
# print(position.market_value())
# print(position.unrealized_pnl())