from  bond import Bond
import pytest
import datetime as dt
@pytest.fixture
def us10y_price_history():
    return [
        (dt.datetime(2026, 1, 1), 98),
        (dt.datetime(2026, 1, 2), 99),
        (dt.datetime(2026, 1, 3), 100),
        ]
@pytest.fixture
def bond(us10y_price_history):
    return Bond(
    "US10Y",
    "US Treasury 10-Year Bond",
    us10y_price_history,
    1000,
    4.25,
    10
)

def test_bond_creation(bond):
    assert bond.ticker == "US10Y"
    assert bond.name == "US Treasury 10-Year Bond"
    assert bond.face_value == 1000
    assert bond.coupon_rate == 4.25
    assert bond.maturity_years == 10

def test_bond_prices(bond):
    p = []

    for timestamp, price in bond.prices:
        p.append(price)

    assert p == [98, 99, 100]

def test_bond_invalid_face_value(us10y_price_history):
    with pytest.raises(
        ValueError,
        match="face_value must be greater than 0"
    ):
        Bond(
            "US10Y",
            "US Treasury 10-Year Bond",
            us10y_price_history,
            - 1000,
            4.25,
            10
        )
@pytest.mark.parametrize("coupon_rate", [0, -1])
def test_bond_invalid_coupon_rate(coupon_rate, us10y_price_history):
    with pytest.raises(
        ValueError,
        match="coupon_rate must be greater than 0"
    ):
        Bond(
            "US10Y",
            "US Treasury 10-Year Bond",
            us10y_price_history,
            1000,
            coupon_rate,
            10
        )

@pytest.mark.parametrize("maturity_years", [0, -1])
def test_bond_invalid_maturity(maturity_years, us10y_price_history):
    with pytest.raises(
        ValueError,
        match= "maturity_years must be greater than 0"
    ):
        Bond(
                "US10Y",
                "US Treasury 10-Year Bond",
                us10y_price_history,
                1000,
                4.25,
                maturity_years
                )
        
def test_bond_str(bond):
    assert str(bond) == "US10Y - US Treasury 10-Year Bond 1000 4.25 10"

def test_annual_coupon_payment(bond):
    assert bond.annual_coupon_payment() == pytest.approx(42.5)


def test_bond_income(bond):
    assert bond.income() == pytest.approx(42.5)