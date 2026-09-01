from asset import Asset
class Portfolio:
    def __init__(self, name):
        if not name or not name.strip():
            raise ValueError("Name can't be empty")

        self._name = name
        self._assets = {}


    @property
    def name(self):
        return self._name

    def add_asset(self, asset, weight):
        # Is asset an Asset?
        if not isinstance(asset, Asset):
            raise TypeError("asset must be an Asset object")
        
        # Is weight valid?
        if not 0 < weight <= 1:
            raise ValueError("Enter a valid weight")

        # Does asset already exist?
        if asset in self._assets:
            raise ValueError("Asset already exists in portfolio")

        # Would total weight exceed 100%?
        current_weight = sum(self._assets.values())
        if current_weight + weight > 1:
            raise ValueError("Total portfolio weight cannot exceed 1")

        self._assets[asset] = weight

    def total_return(self):
        if not self._assets:
            return 0.0
        portfolio_return  = 0.0
        for asset, weight in self._assets.items():
            portfolio_return  += asset.total_return() * weight

        return portfolio_return 
    
apple = Asset("AAPL", "Apple Inc.", [100, 105, 110])

microsoft = Asset("MSFT", "Microsoft Corp.", [200, 205, 210])

google = Asset("GOOGL", "Alphabet Inc.", [150, 155, 160])

portfolio = Portfolio("Tech Portfolio")

portfolio.add_asset(apple, 0.40)
portfolio.add_asset(microsoft, 0.35)
portfolio.add_asset(google, 0.25)

print(portfolio.total_return())


