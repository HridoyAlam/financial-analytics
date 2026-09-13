import pytest
# from asset import Asset
from stock import Stock
import datetime as dt

@pytest.fixture
def price_history():
    return [
    (dt.datetime(2026, 1, 1), 100),
    (dt.datetime(2026, 1, 2), 105),
    (dt.datetime(2026, 1, 3), 110),
]

@pytest.fixture
def asset(price_history):
    return Stock(
        "AAPL",
        "Apple Inc.",
        price_history,
        "Technology",
        2.0
    )

def test_asset_creation(asset, price_history):
    assert asset.ticker == "AAPL"
    assert asset.name == "Apple Inc."
    assert asset.prices == price_history

def test_current_price(asset):
    assert asset.current_price() == 110

def test_total_return(asset):
    assert asset.total_return() == pytest.approx(0.10)

def test_total_return_percent(asset):
    assert asset.total_return_percent() == pytest.approx(10.0)

@pytest.mark.parametrize("ticker", ["", " "])
def test_asset_invalid_ticker(ticker, price_history):
    with pytest.raises(
        ValueError,
        match="Ticker can't be empty"
    ):
        Stock(
            ticker,
            "Apple Inc.",
            price_history,
            "Technology",
            2.0
    )
@pytest.mark.parametrize("name", ["", " "])
def test_asset_invalid_name(name, price_history):
    with pytest.raises(
        ValueError,
        match="Name can't be empty"
    ):
        Stock(
                "AAPL",
                name,
                price_history,
                "Technology",
                2.0
            )

def test_asset_empty_prices():
    with pytest.raises(ValueError, match="Prices can't be empty"):
         Stock(
                "AAPL",
                "Apple Inc.",
                [],
                "Technology",
                2.0
                )
# @pytest.mark.parametrize("price", [0, -1])
def test_asset_invalid_prices():
    with pytest.raises(ValueError, match="Price must be greater than 0"):
        Stock(
            "AAPL",
            "Apple Inc.",
            [(dt.datetime(2026, 1, 3), -110),
            (dt.datetime(2026, 1, 1), 100)],
            "Technology",
            2.0
        )

def test_asset_protection(asset, price_history):
    prices = asset.prices
    prices.append(9999)
    assert asset.prices == price_history

def test_asset_str(asset):
    assert str(asset) == "AAPL - Apple Inc. (Technology)"


def test_price_history_must_be_chronological():
     with pytest.raises(
            ValueError,
            match="Price history timestamps must be in strictly increasing order"
        ):
            Stock(
                "AAPL",
                "Apple Inc.",
                [(dt.datetime(2026, 1, 3), 110),
                (dt.datetime(2026, 1, 1), 100)],
                "Technology",
                2.0
            )

def test_price_at_exact_timestamp(asset):
    assert asset.price_at((dt.datetime(2026, 1, 3))) == 110

def test_price_at_invalid_timestamp(asset):
    with pytest.raises(
        TypeError,
        match= "timestamp must be a datetime"
    ):
        asset.price_at((2026, 1, 3))

def test_price_at_timestamp_not_found(asset):
    timestamp = dt.datetime(2025, 1, 4)
    with pytest.raises(
        ValueError,
        match= f"No price found for timestamp {timestamp}"
    ):
        asset.price_at(timestamp)

def test_price_at_timestamp_between_prices(asset):
    timestamp = dt.datetime(2026, 1, 2, 12)

    assert asset.price_at(timestamp) == 105

def test_price_at_after_last_price(asset):
    timestamp = dt.datetime(2026, 1, 4)

    assert asset.price_at(timestamp) == 110

def test_price_at_before_first_price(asset):
    timestamp = dt.datetime(2025, 12, 31)

    with pytest.raises(
        ValueError,
        match=f"No price found for timestamp {timestamp}"
    ):
        asset.price_at(timestamp)