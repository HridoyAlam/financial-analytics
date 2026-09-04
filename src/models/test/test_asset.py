import pytest
from asset import Asset
@pytest.fixture
def asset():
    return Asset(
        "AAPL",
        "Apple Inc.",
        [100, 105, 110]
    )

def test_asset_creation(asset):
    assert asset.ticker == "AAPL"
    assert asset.name == "Apple Inc."
    assert asset.prices == [100, 105, 110]

def test_current_price(asset):
    assert asset.current_price() == 110

def test_total_return(asset):
    assert asset.total_return() == pytest.approx(0.10)

def test_total_return_percent(asset):
    assert asset.total_return_percent() == pytest.approx(10.0)

@pytest.mark.parametrize("ticker", ["", " "])
def test_asset_invalid_ticker(ticker):
    with pytest.raises(
        ValueError,
        match="Ticker can't be empty"
    ):
        Asset(
            ticker,
            "Apple Inc.",
            [100, 105, 110]
        )
@pytest.mark.parametrize("name", ["", " "])
def test_asset_invalid_name(name):
    with pytest.raises(
        ValueError,
        match="Name can't be empty"
    ):
        Asset(
            "AAPL",
            name,
            [100, 105, 110]
        )

def test_asset_empty_prices():
    with pytest.raises(ValueError, match="Prices can't be empty"):
        Asset(
            "AAPL",
            "Apple Inc.",
            []
        )
@pytest.mark.parametrize("price", [0, -1])
def test_asset_invalid_prices(price):
    with pytest.raises(ValueError, match="Price must be greater than 0"):
        Asset(
            "AAPL",
            "Apple Inc.",
            [price]
        )

def test_asset_protection(asset):
    prices = asset.prices
    prices.append(9999)
    assert asset.prices == [100, 105, 110]

def test_asset_str(asset):
    assert str(asset) == "AAPL - Apple Inc."