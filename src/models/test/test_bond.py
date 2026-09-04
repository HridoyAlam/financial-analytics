from  bond import Bond
import pytest
@pytest.fixture
def bond():
    return Bond(
    "US10Y",
    "US Treasury 10-Year Bond",
    [98, 99, 100],
    1000,
    4.25,
    10
)

def test_bond_creation(bond):
    assert bond.ticker == "US10Y"
    assert bond.name == "US Treasury 10-Year Bond"
    assert bond.prices == [98, 99, 100]
    assert bond.face_value == 1000
    assert bond.coupon_rate == 4.25
    assert bond.maturity_years == 10

def test_bond_invalid_face_value():
    with pytest.raises(
        ValueError,
        match="face_value must be greater than 0"
    ):
        Bond(
            "US10Y",
            "US Treasury 10-Year Bond",
            [98, 99, 100],
            - 1000,
            4.25,
            10
        )
@pytest.mark.parametrize("coupon_rate", [0, -1])
def test_bond_invalid_coupon_rate(coupon_rate):
    with pytest.raises(
        ValueError,
        match="coupon_rate must be greater than 0"
    ):
        Bond(
            "US10Y",
            "US Treasury 10-Year Bond",
            [98, 99, 100],
            1000,
            coupon_rate,
            10
        )

@pytest.mark.parametrize("maturity_years", [0, -1])
def test_bond_invalid_maturity(maturity_years):
    with pytest.raises(
        ValueError,
        match= "maturity_years must be greater than 0"
    ):
        Bond(
                "US10Y",
                "US Treasury 10-Year Bond",
                [98, 99, 100],
                1000,
                4.25,
                maturity_years
                )
        
def test_bond_str(bond):
    assert str(bond) == "US10Y - US Treasury 10-Year Bond 1000 4.25 10"

def test_annual_coupon_payment(bond):
    assert bond.annual_coupon_payment() == pytest.approx(42.5)