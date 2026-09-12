from cash_flow import CashFlow
import pytest

@pytest.mark.parametrize("param", ["deposit", "Deposit", "DEPOSIT"])
def test_valid_deposit(param):
    cash_flow = CashFlow(
        10,
        param
    )
    assert cash_flow.amount == 10
    assert cash_flow.flow_type == "DEPOSIT"

@pytest.mark.parametrize("param", ["withdrawal", "Withdrawal", "WITHDRAWAL"])
def test_valid_withdrawal(param):
    cash_flow = CashFlow(
        10,
        param
    )
    assert cash_flow.flow_type == "WITHDRAWAL"

def test_invalid_amount_withdrawal():
    with pytest.raises(
        ValueError,
        match="Amount must be greater than 0"
    ):
        CashFlow(
            0,
            "WITHDRAWAL"
        )
def test_invalid_amount_deposit():
    with pytest.raises(
        ValueError,
        match="Amount must be greater than 0"
    ):
        CashFlow(
            0,
            "DEPOSIT"
        )
def test_invalid_flow_type():
    with pytest.raises(
        ValueError,
        match="Flow type must be either Deposit or Withdrawal"
    ):
        CashFlow(
            100,
            "Deport"
        )
