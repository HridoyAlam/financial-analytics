class CashFlow:

    def __init__(self, amount: float, flow_type: str) -> None:

        if amount <= 0:
            raise ValueError("Amount must be greater than 0")

        if flow_type.upper() not in ["DEPOSIT", "WITHDRAWAL"]:
            raise ValueError("Flow type must be either Deposit or Withdrawal")

        self._amount = amount
        self._flow_type = flow_type.upper()

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def flow_type(self) -> str:
        return self._flow_type

        
    