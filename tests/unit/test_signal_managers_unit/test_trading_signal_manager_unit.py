import pytest

from robothood.discord_signals.signals import TradingSignal
from robothood.errors.errors import UnknownBaseAsset, UnknownPairError, WrongSignalError
from robothood.signal_managers.constants import BASE_ASSETS_INFO
from robothood.signal_managers.trading_signal_manager import TradingSignalManager
from tests.conftest import (  # pylint:disable=import-error
    TRADING_SIGNALS,
    mock_trading_signal_manager,
)


@pytest.mark.parametrize(
    "trading_signal, wrong_signal, pair, market_price, base_asset_balance, oco_allowed, min_qty, "
    "step_size, tick_size, unknown_pair, unknown_base_asset",
    [
        (
            TRADING_SIGNALS["FRONTBTC"],
            False,
            "FRONTBTC",
            0.00016,
            0.02,
            True,
            0.1,
            0.2,
            0.3,
            False,
            False,
        ),
        (
            TRADING_SIGNALS["AUDIOBTC"],
            False,
            "AUDIOBTC",
            0.003,
            0.0072,
            False,
            0.871,
            0.985,
            0.156,
            False,
            False,
        ),
        (
            TRADING_SIGNALS["KAVAUSDT"],
            False,
            "KAVAUSDT",
            44.8,
            289,
            True,
            0.1,
            0.2,
            0.3,
            False,
            False,
        ),
        (
            TRADING_SIGNALS["LTCUSDT"],
            False,
            "LTCUSDT",
            16.3,
            7,
            False,
            0.871,
            0.985,
            0.156,
            False,
            False,
        ),
        (
            TradingSignal(
                timestamp="2020-11-01 13:00",
                quote_currency="Unknown Quote",
                base_currency="BTC",
                buy_around="1340",
                targets=["1375", "1435", "1550", "1700"],
                stop_loss="980",
            ),
            False,
            "Unknown Pair",
            0.003,
            0.0072,
            False,
            0.871,
            0.985,
            0.156,
            True,
            False,
        ),
        (
            TradingSignal(
                timestamp="2022-12-02 08:15",
                quote_currency="BNB",
                base_currency="UKN",
                buy_around="260",
                targets=["264", "290", "320", "365"],
                stop_loss="180",
            ),
            False,
            "Unknown Pair",
            0.003,
            0.0072,
            False,
            0.871,
            0.985,
            0.156,
            False,
            True,
        ),
        (None, True, None, None, None, None, None, None, None, False, False),
        ("Hello", True, None, None, None, None, None, None, None, False, False),
        (16, True, None, None, None, None, None, None, None, False, False),
    ],
    ids=[
        "first-valid-trading-signal-btc",
        "second-valid-trading-signal-btc",
        "first-valid-trading-signal-usdt",
        "second-valid-trading-signal-usdt",
        "unknown-pair",
        "unknown-base-asset",
        "invalid-type-none",
        "invalid-type-string",
        "invalid-type-int",
    ],
)
def test_init(
    mocker,
    trading_signal,
    wrong_signal,
    pair,
    market_price,
    base_asset_balance,
    oco_allowed,
    min_qty,
    step_size,
    tick_size,
    unknown_pair,
    unknown_base_asset,
):
    (
        get_ticker_mock,
        get_asset_balance_mock,
        get_symbol_info_mock,
        convert_ts_mock,
    ) = mock_trading_signal_manager(
        mocker=mocker,
        market_price=market_price,
        asset_balances=base_asset_balance,
        pair=pair,
        oco_allowed=oco_allowed,
        min_qty=min_qty,
        step_size=step_size,
        tick_size=tick_size,
        unknown_pair=unknown_pair,
    )

    min_buy_mock_return_val = 0.00015
    maxbuy_mock_return_val = 168
    compute_buy_min_max_mock = mocker.patch(
        "robothood.signal_managers.trading_signal_manager.compute_buy_min_max",
        return_value=(min_buy_mock_return_val, maxbuy_mock_return_val),
    )

    if wrong_signal:
        with pytest.raises(WrongSignalError) as e:
            TradingSignalManager(signal=trading_signal)
        assert (
            str(e.value) == "TradingSignalManager only accepts TradingSignal as signal: your "
            f"signal type is {type(trading_signal)}"
        )

    elif unknown_pair:
        with pytest.raises(UnknownPairError) as e:
            TradingSignalManager(signal=trading_signal)
        assert str(e.value) == f"Pair {trading_signal.pair} does not exist in Binance"

    elif unknown_base_asset:
        with pytest.raises(UnknownBaseAsset) as e:
            TradingSignalManager(signal=trading_signal)
        assert (
            str(e.value) == f"Base asset {trading_signal.base_currency} is not known or not "
            "managed by this bot yet."
        )

    else:
        manager = TradingSignalManager(signal=trading_signal)

        get_ticker_mock.assert_called_once_with(symbol=pair)
        convert_ts_mock.assert_called_once_with(
            message_signal=trading_signal, market_price=manager.market_price
        )
        get_asset_balance_mock.assert_called_once_with(asset=trading_signal.base_currency)
        get_symbol_info_mock.assert_called_once_with(symbol=pair)
        compute_buy_min_max_mock.assert_called_once_with(
            buy_around=manager.signal.buy_around,
            first_target=min(manager.signal.targets),
            tick_size=tick_size,
        )

        assert manager.market_price == market_price
        assert (
            manager.available_base_asset_fonds
            == base_asset_balance - BASE_ASSETS_INFO[trading_signal.base_currency]["min_balance"]
        )
        assert manager.oco_allowed is oco_allowed
        assert manager.min_qty == min_qty
        assert manager.step_size == step_size
        assert manager.tick_size == tick_size
        assert manager.signal == trading_signal
        assert manager.max_buy > manager.min_buy
        assert manager.min_buy == min_buy_mock_return_val
        assert manager.max_buy == maxbuy_mock_return_val


def test_check_if_ready_processs(mocker):
    mock_trading_signal_manager(mocker=mocker)
    manager = TradingSignalManager(signal=TRADING_SIGNALS["FRONTBTC"])
    result = manager.check_if_ready_to_process()

    assert result


def test_calculate_buy_quantity(mocker):
    mock_trading_signal_manager(mocker=mocker)
    manager = TradingSignalManager(signal=TRADING_SIGNALS["FRONTBTC"])
    buy_quantity = manager.calculate_buy_quantity()
    assert buy_quantity == 42


def test_calculate_sell_quantity(mocker):
    mock_trading_signal_manager(mocker=mocker)
    manager = TradingSignalManager(signal=TRADING_SIGNALS["FRONTBTC"])
    sell_quantities = manager.calculate_sell_quantities()
    assert sell_quantities == {"T1": 42, "T2": 0, "T3": 0, "T4": 0}


def test_compute_sell_parameters(mocker):
    mock_trading_signal_manager(mocker=mocker)
    manager = TradingSignalManager(signal=TRADING_SIGNALS["FRONTBTC"])
    sell_price, stop_price, limit_price = manager.compute_sell_parameters()

    assert sell_price == {"T1": "42", "T2": "0", "T3": "0", "T4": "0"}
    assert stop_price == "42"
    assert limit_price == "42"


def test_process_signal(mocker):
    mock_trading_signal_manager(mocker=mocker)
    manager = TradingSignalManager(signal=TRADING_SIGNALS["FRONTBTC"])
    assert manager.process_signal() is None
