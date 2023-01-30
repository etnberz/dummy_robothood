import os

import pytest

from robothood.discord_signals.signals import TargetReachedSignal, TradingSignal
from robothood.signal_managers.constants import BASE_ASSETS_INFO


def pytest_configure(config):
    config.addinivalue_line("markers", "no_env_var: mark test to not use env var mock")


@pytest.fixture(autouse=True)
def mock_env_variables(request):
    if not request.node.get_closest_marker("no_profiling"):
        os.environ["BAPI_KEY"] = ""
        os.environ["BAPI_SECRET"] = ""
    yield


class TestClient:
    def __init__(self):
        pass

    def get_ticker(self, symbol):
        pass

    def get_asset_balance(self, symbol):
        pass

    def get_symbol_info(self, symbol):
        pass

    def order_market_buy(self, symbol, quantity):
        pass

    def get_order(self, symbol, orderId):
        pass

    def order_oco_sell(
        self, symbol, quantity, price, stopPrice, stopLimitPrice, stopLimitTimeInForce
    ):
        pass


TARGET_REACHED_SIGNALS = {
    "FRONTBTC": TargetReachedSignal(
        timestamp="2020-11-01 13:00",
        pair="FRONTBTC",
        target_num="1",
    ),
    "AUDIOBTC": TargetReachedSignal(
        timestamp="2020-11-01 13:00",
        pair="AUDIOBTC",
        target_num="2",
    ),
    "LUNABTC": TargetReachedSignal(
        timestamp="2020-11-01 13:00",
        pair="LUNABTC",
        target_num="3",
    ),
    "GTOBTC": TargetReachedSignal(
        timestamp="2020-11-01 13:00",
        pair="GTOBTC",
        target_num="4",
    ),
    "ETHBTC": TargetReachedSignal(
        timestamp="2020-11-01 13:00",
        pair="ETHBTC",
        target_num="1",
    ),
    "LTCUSDT": TargetReachedSignal(
        timestamp="2020-11-01 13:00",
        pair="LTCUSDT",
        target_num="1",
    ),
}

TRADING_SIGNALS = {
    "FRONTBTC": TradingSignal(
        timestamp="2020-11-01 13:00",
        quote_currency="FRONT",
        base_currency="BTC",
        buy_around="1340",
        targets=["1375", "1435", "1550", "1700"],
        stop_loss="980",
    ),
    "AUDIOBTC": TradingSignal(
        timestamp="2020-11-01 13:00",
        quote_currency="AUDIO",
        base_currency="BTC",
        buy_around="1340",
        targets=["1375", "1435", "1550", "1700"],
        stop_loss="980",
    ),
    "LUNABTC": TradingSignal(
        timestamp="2020-11-01 13:00",
        quote_currency="LUNA",
        base_currency="BTC",
        buy_around="12100",
        targets=["12600", "12990", "13700", "15800"],
        stop_loss="8500",
    ),
    "GTOBTC": TradingSignal(
        timestamp="2020-11-01 13:00",
        quote_currency="GTO",
        base_currency="BTC",
        buy_around="92",
        targets=["94", "98", "110", "115"],
        stop_loss="75",
    ),
    "ETHBTC": TradingSignal(
        timestamp="2020-11-01 13:00",
        quote_currency="ETH",
        base_currency="BTC",
        buy_around="6936000",
        targets=["6940000", "6941000", "6942000", "6943000"],
        stop_loss="6926000",
    ),
    "KAVAUSDT": TradingSignal(
        timestamp="2020-11-01 13:00",
        quote_currency="KAVA",
        base_currency="USDT",
        buy_around="0.837",
        targets=["0.845", "0.876", "0.950", "0.990"],
        stop_loss="0.6800",
    ),
    "LTCUSDT": TradingSignal(
        timestamp="2020-11-01 13:00",
        quote_currency="LTC",
        base_currency="USDT",
        buy_around="61.26",
        targets=["61.90", "65.00", "69.00", "72.00"],
        stop_loss="40.00",
    ),
    "ALGOUSDT": TradingSignal(
        timestamp="2020-11-01 13:00",
        quote_currency="ALGO",
        base_currency="USDT",
        buy_around="0.2903",
        targets=["0.2932", "0.2990", "0.3120", "0.3200"],
        stop_loss="0.2000",
    ),
}


def mock_trading_signal_manager(
    mocker,
    market_price=0.069,
    pair="ETHBTC",
    trading_signal=None,
    asset_balances=BASE_ASSETS_INFO["BTC"]["invest_batch"] + 1,
    oco_allowed=True,
    min_qty=0.01,
    step_size=0.01,
    tick_size=1e-8,
    unknown_pair=False,
):
    if trading_signal is None and pair in TRADING_SIGNALS:
        trading_signal = TRADING_SIGNALS[pair]

    mocker.patch(
        "robothood.signal_managers.signal_manager.Client",
        return_value=TestClient(),
    )

    get_ticker_mock = mocker.patch(
        "tests.conftest.TestClient.get_ticker",
        return_value={"lastPrice": str(market_price)},
    )

    convert_ts_mock = mocker.patch(
        "robothood.signal_managers.trading_signal_manager.convert_trading_signal",
        return_value=trading_signal,
    )

    if isinstance(asset_balances, list):
        get_asset_balance_mock = mocker.patch(
            "tests.conftest.TestClient.get_asset_balance",
            side_effect=[{"free": str(balance)} for balance in asset_balances],
        )
    else:
        get_asset_balance_mock = mocker.patch(
            "tests.conftest.TestClient.get_asset_balance",
            return_value={"free": str(asset_balances)},
        )
    get_symbol_info_mock = mocker.patch(
        "tests.conftest.TestClient.get_symbol_info",
        return_value=None
        if unknown_pair
        else {
            "symbol": pair,
            "ocoAllowed": oco_allowed,
            "filters": [
                {
                    "filterType": "LOT_SIZE",
                    "minQty": str(min_qty),
                    "stepSize": str(step_size),
                },
                {"filterType": "PRICE_FILTER", "tickSize": str(tick_size)},
            ],
        },
    )
    return get_ticker_mock, get_asset_balance_mock, get_symbol_info_mock, convert_ts_mock
