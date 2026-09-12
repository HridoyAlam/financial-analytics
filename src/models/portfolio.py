from asset import Asset
from stock import Stock
from position import Position
from transaction import Transaction
from cash_flow import CashFlow
class Portfolio:
    def __init__(self, name: str, initial_capital: float):

        if not name or not name.strip():
            raise ValueError("Name can't be empty")

        if initial_capital <= 0:
            raise ValueError("initial_capital must be greater than zero")

        self._name = name
        self._initial_capital = initial_capital
        self._positions: dict[Asset, Position] =  {}

        self._cash = initial_capital


    @property
    def name(self) -> str:
        return self._name

    @property
    def initial_capital(self) -> float:
        return self._initial_capital

    @property
    def positions(self) -> dict[Asset, Position]:
        return self._positions.copy()

    @property
    def cash(self) -> float:
        return self._cash
    
    def add_position(self, position: Position) -> None:

        if not isinstance(position, Position):
            raise TypeError("position must be a Position-object")
        
        if position.asset in self._positions:
            raise ValueError("Asset already exists in portfolio")

        if position.cost_basis() > self._cash:
            raise ValueError("Insufficient capital")

        self._positions[position.asset] = position
        self._cash -= position.cost_basis()

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

    
    def total_income(self) -> float:

        total = 0.0
        for position in self._positions.values():
            total += position.income()
        return total

    def allocation(self, asset: Asset) -> float:

        if  asset not in self._positions:
            raise ValueError("Asset not found in portfolio")

        position = self._positions[asset]
        cost_basis = position.cost_basis()
        return cost_basis / self.initial_capital * 100

    def available_cash(self) -> float:
        return self._cash

    def remove_position(self, asset: Asset) -> None:
            if asset not in self._positions:
                raise ValueError("Asset not found in portfolio")
            
            del self._positions[asset]

    def position_weight(self, asset: Asset) -> float:

        if  asset not in self._positions:
            raise ValueError("Asset not found in portfolio")

        position = self._positions[asset]
        cost_basis = position.cost_basis()

        return cost_basis / self.total_cost() * 100

    def apply_transaction(self, transaction: Transaction) -> None:
        if transaction.asset not in self._positions:
            raise ValueError("Asset not found in portfolio")

        position = self._positions[transaction.asset]
        position.apply_transaction(transaction)

        if transaction.transaction_type == "SELL":
            self._cash += transaction.total_value()
    
        if transaction.transaction_type == "BUY":
            self._cash -= transaction.total_value()

    def apply_cash_flow(self, cash_flow: CashFlow) -> None:
        if cash_flow.flow_type == "DEPOSIT":
            self._cash += cash_flow.amount

        elif cash_flow.flow_type == "WITHDRAWAL":
            if self._cash < cash_flow.amount:
                raise ValueError("Withdrawal exceeding available cash")

            self._cash -= cash_flow.amount

    def active_positions(self) -> list[Position]:
        active_positions = []
        for position in self._positions.values():
            if position.is_active:
                active_positions.append(position)
        return active_positions
    
    def closed_positions(self) -> list[Position]:
        closed_positions = []

        for position in self._positions.values():
            if not position.is_active:
                closed_positions.append(position) 
        return closed_positions

    def realized_pnl(self) -> float:
        total = 0.0

        for position in self._positions.values():
            total += position.realized_pnl

        return total

    def combined_pnl(self) -> float:
        return self.realized_pnl() + self.total_pnl()

    
    
apple = Stock(
        "AAPL",
        "Apple Inc.",
        [100, 105, 110],
        "Technology",
        2.0
    )

apple_position = Position(
            apple,
            quantity=100,
            average_cost=200
    )


portfolio = Portfolio("Tech Portfolio", 30000)

portfolio.add_position(apple_position)

print(portfolio.total_pnl())
print(portfolio.total_cost())
print(portfolio.current_value())
print(f"{portfolio.total_return():.2%}")

print(portfolio.total_income())
print(portfolio.allocation(apple))
print(f"available_cash:{portfolio.available_cash()}")

# portfolio.remove_position(apple)
# print(portfolio.available_cash())
print(portfolio.position_weight(apple))

# buy_transaction = Transaction(
#     apple,
#     "BUY",
#     50,
#     180
# )
# portfolio.apply_transaction(buy_transaction)
# print(f"after buy available_cash:{portfolio.available_cash()}")


# sell_transaction = Transaction(
#     apple,
#     "SELL",
#     50,
#     220
# )
# portfolio.apply_transaction(sell_transaction)
# print(apple_position.quantity)
# print(apple_position.realized_pnl)
# print(f"after sell available_cash:{portfolio.available_cash()}")


