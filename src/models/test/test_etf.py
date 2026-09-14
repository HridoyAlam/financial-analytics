from etf import ETF
import datetime as dt
import pytest
@pytest.fixture
def spy_price_history():
    return [
    (dt.datetime(2026, 1, 1), 500),
    (dt.datetime(2026, 1, 2), 510),
    (dt.datetime(2026, 1, 3), 520),
]
@pytest.fixture
def etf(spy_price_history):
    return ETF(
        "SPY",
        "SPDR S&P 500 ETF",
        spy_price_history,
        0.0945,
        7.0
    )


def test_etf_invalid_expense_ratio(spy_price_history):
    with pytest.raises(
        ValueError,
        match="expense_ratio must be greater than zero"
    ):
        ETF(
        "SPY",
        "SPDR S&P 500 ETF",
        spy_price_history,
        -0.0945,
        7.0
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

def test_etf_income(etf):
    assert etf.income() == pytest.approx(7.0)

def test_invalid_annual_distribution(spy_price_history):
    with pytest.raises(
        ValueError,
        match="annual distribution can't be negative"
    ):
        ETF(
                "SPY",
                "SPDR S&P 500 ETF",
                spy_price_history,
                0.0945,
                -7.0
            )
        