from etf import ETF
import pytest
@pytest.fixture
def etf():
    return ETF(
        "SPY",
        "SPDR S&P 500 ETF",
        [500, 510, 520],
        0.0945
    )


def test_etf_invalid_expense_ratio():
    with pytest.raises(
        ValueError,
        match="expense_ratio must be greater than zero"
    ):
         ETF(
        "SPY",
        "SPDR S&P 500 ETF",
        [500, 510, 520],
        -0.0945
    )

def test_etf_creation(etf):
    assert etf.ticker == "SPY"
    assert etf.name == "SPDR S&P 500 ETF"
    assert etf.current_price() == 520
    assert etf.total_return() == pytest.approx(.04)
    assert etf.expense_ratio == pytest.approx(0.0945)

def test_etf_str(etf):
    # just etf is a object, that's it have to wrap with str
    assert str(etf) == "SPY - SPDR S&P 500 ETF  0.0945"

