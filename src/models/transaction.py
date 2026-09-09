from asset import Asset
class Transaction():
    def __init__(
            self, 
            asset:Asset, 
            transaction_type: str, 
            quantity: float,
            price: float
            ) -> None:

        if not isinstance(asset, Asset):
            raise TypeError("asset must be an instance of Asset")

        if transaction_type.upper() not in ["BUY", "SELL"]:
            raise ValueError("Transaction type must either BUY or SELL")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        
        if price <= 0:
            raise ValueError("Price must be greater than zero")

        self._asset = asset
        self._transaction_type = transaction_type.upper()
        self._quantity = quantity
        self._price = price

    @property
    def asset(self) -> Asset:
        return self._asset
    
    @property
    def transaction_type(self) -> str:
        return self._transaction_type
    
    @property
    def quantity(self) -> float:
        return self._quantity
    
    @property
    def price(self) -> float:
        return self._price

    def total_value(self) -> float:
        return self.quantity * self.price

    