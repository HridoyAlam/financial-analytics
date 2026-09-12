import datetime as dt  
class CashFlow:

    def __init__(self, amount: float, flow_type: str, timestamp: dt.datetime) -> None:

        if amount <= 0:
            raise ValueError("Amount must be greater than 0")

        if flow_type.upper() not in ["DEPOSIT", "WITHDRAWAL"]:
            raise ValueError("Flow type must be either Deposit or Withdrawal")

        if not isinstance(timestamp, dt.datetime):
            raise TypeError("timestamp must be a datetime")

        self._amount = amount
        self._flow_type = flow_type.upper()
        self._timestamp = timestamp

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def flow_type(self) -> str:
        return self._flow_type

    @property 
    def timestamp(self) -> dt.datetime:
        return self._timestamp

        
    