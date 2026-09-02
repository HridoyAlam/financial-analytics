from asset import Asset

class Position:
    def __init__(self, asset, quantity, average_cost):
        if not isinstance(asset, Asset):
            raise TypeError("asset must be an instance of Asset")

        if quantity <= 0:
            raise ValueError("Quantity must greater than zero")
        
        if average_cost <= 0:
            raise ValueError("Average cost must greater than zero")

        self._asset = asset
        self._quantity = quantity
        self._average_cost = average_cost

    @property
    def asset(self):
        return self._asset

    @property
    def quantity(self):
        return self._quantity

    @property
    def average_cost(self):
        return self._average_cost

    def cost_basis(self):
        return self.quantity * self.average_cost

apple = Asset(
    "AAPL",
    "Apple Inc.",
    [100, 105, 110]
)

position = Position(
    asset=apple,
    quantity=100,
    average_cost=100
)

print(position.asset)
print(position.quantity)
print(position.average_cost)
print(position.cost_basis())