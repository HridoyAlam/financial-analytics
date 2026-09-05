from asset import Asset
from position import Position
class Portfolio:
    def __init__(self, name: str, initial_capital: float):

        if not name or not name.strip():
            raise ValueError("Name can't be empty")

        if initial_capital <= 0:
            raise ValueError("initial_capital must be greater than zero")

        self._name = name
        self._initial_capital = initial_capital
        self._positions: dict[Asset, Position] =  {}


    @property
    def name(self) -> str:
        return self._name

    @property
    def initial_capital(self) -> float:
        return self._initial_capital

    @property
    def positions(self) -> dict[Asset, Position]:
        return self._positions.copy()
    
    def add_position(self, position: Position) -> None:

        if not isinstance(position, Position):
            raise TypeError("position must be a Position-object")
        
        if position.asset in self._positions:
            raise ValueError("Asset already exists in portfolio")

        current_cost = 0.0
        for existing_position in self._positions.values():
            current_cost += existing_position.cost_basis()

        if current_cost + position.cost_basis() > self.initial_capital:
            raise ValueError("Insufficient capital")

        self._positions[position.asset] = position

    def current_value(self) -> float:
        total = 0.0

        for position in self._positions.values():
            total += position.market_value()

        return total

    def total_pnl(self) -> float:
        total = 0.0

        for position in self._positions.values():
            total += position.unrealized_pnl()

        return total
    def total_cost(self) -> float:
        total = 0.0

        for position in self._positions.values():
            total += position.cost_basis()

        return total
    
    
    def total_return(self) -> float:
        total_cost = self.total_cost()
        if total_cost == 0:
            return 0.0
        
        return (self.total_pnl() / total_cost) 

    
apple = Asset(
    "AAPL",
    "Apple Inc.",
    [100, 105, 110]
)
microsoft = Asset(
    "MSFT",
    "Microsoft Corp.",
    [200, 205, 210]
)

apple_position = Position(
    apple,
    quantity=100,
    average_cost=100
)

microsoft_position = Position(
    microsoft,
    quantity=20,
    average_cost=200
)

portfolio = Portfolio("Tech Portfolio", 100000)

portfolio.add_position(microsoft_position)
portfolio.add_position(apple_position)

# print(portfolio.total_pnl())
# print(portfolio.total_cost())
# print(portfolio.current_value())
# print(f"{portfolio.total_return():.2%}")