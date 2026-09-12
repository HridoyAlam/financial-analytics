from cash_flow import CashFlow
import pytest
import datetime as dt

@pytest.mark.parametrize("param", ["deposit", "Deposit", "DEPOSIT"])
def test_valid_deposit(param):
    cash_flow = CashFlow(
        10,
        param,
        dt.datetime(2026, 1, 1)
    )
    assert cash_flow.amount == 10
    assert cash_flow.flow_type == "DEPOSIT"

@pytest.mark.parametrize("param", ["withdrawal", "Withdrawal", "WITHDRAWAL"])
def test_valid_withdrawal(param):
    cash_flow = CashFlow(
        10,
        param,
        dt.datetime(2026, 1, 1)
    )
    assert cash_flow.flow_type == "WITHDRAWAL"

def test_invalid_amount_withdrawal():
    with pytest.raises(
        ValueError,
        match="Amount must be greater than 0"
    ):
        CashFlow(
            0,
            "WITHDRAWAL",
            dt.datetime(2026, 1, 1)
        )
def test_invalid_amount_deposit():
    with pytest.raises(
        ValueError,
        match="Amount must be greater than 0"
    ):
        CashFlow(
            0,
            "DEPOSIT",
            dt.datetime(2026, 1, 1)
        )
def test_invalid_flow_type():
    with pytest.raises(
        ValueError,
        match="Flow type must be either Deposit or Withdrawal"
    ):
        CashFlow(
            100,
            "Deport",
            dt.datetime(2026, 1, 1)
        )
def test_invalid_timestamp():
    with pytest.raises(
        TypeError,
        match="timestamp must be a datetime"
    ):
        CashFlow(
            100,
            "DEPOSIT",
            "2026-1-1"
        )
def test_valid_timestamp():
    timestamp = dt.datetime(2026, 1, 1)

    cash_flow = CashFlow(
        100,
        "DEPOSIT",
        timestamp
    )

    assert cash_flow.timestamp == timestamp