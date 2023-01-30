import pytest

from robothood.discord_signals.signals import TradingSignal
from robothood.signal_managers.utils import (
    compute_buy_min_max,
    convert_price_message_to_real_price,
    convert_trading_signal,
)


@pytest.mark.parametrize(
    "signal_price, market_price, expected_price",
    [
        (130, 0.00000210, 0.00000130),
        (10.2, 21.59, 10.2),
        (1.39, 21.59, 1.39),
        (80.9, 21.59, 80.9),
        (435, 0.0000436, 0.0000435),
        (2540.1, 0.02539, 0.025401),
        (5020.8, 0.02539, 0.050208),
        (99, 0.001, 0.00099),
        (21.6, 21.59, 21.6),
        (1911, 1.912e-5, 1.911e-05),
        (210, 0.00000210, 0.00000210),
        (400, 6.85e-6, 4e-6),
    ],
)
def test_convert_price_message_to_real_price(signal_price, market_price, expected_price):
    result = convert_price_message_to_real_price(
        signal_price=signal_price, market_price=market_price
    )
    assert result == expected_price


@pytest.mark.parametrize(
    "trading_signal, market_price, expected_signal",
    [
        (
            TradingSignal(
                timestamp="2020-11-01 13:00",
                quote_currency="FRONT",
                base_currency="BTC",
                buy_around="1340",
                targets=["1375", "1435", "1550", "1700"],
                stop_loss="980",
            ),
            0.0001339,
            TradingSignal(
                timestamp="2020-11-01 13:00",
                quote_currency="FRONT",
                base_currency="BTC",
                buy_around="0.0001340",
                targets=["0.0001375", "0.0001435", "0.0001550", "0.0001700"],
                stop_loss="0.0000980",
            ),
        ),
        (
            TradingSignal(
                timestamp="2020-11-01 13:00",
                quote_currency="KAVA",
                base_currency="USDT",
                buy_around="0.837",
                targets=["0.845", "0.876", "0.950", "0.990"],
                stop_loss="0.6800",
            ),
            0.837,
            TradingSignal(
                timestamp="2020-11-01 13:00",
                quote_currency="KAVA",
                base_currency="USDT",
                buy_around="0.837",
                targets=["0.845", "0.876", "0.950", "0.990"],
                stop_loss="0.6800",
            ),
        ),
    ],
    ids=["FRONTBTC", "KAVAUSDT"],
)
def test_convert_trading_signal(mocker, trading_signal, market_price, expected_signal):
    args = [trading_signal.buy_around] + trading_signal.targets + [trading_signal.stop_loss]
    side_effect = (
        [expected_signal.buy_around] + expected_signal.targets + [expected_signal.stop_loss]
    )
    side_effect = [float(se) for se in side_effect]
    convert_price_mock = mocker.patch(
        "robothood.signal_managers.utils.convert_price_message_to_real_price",
        side_effect=side_effect,
    )

    converted_signal = convert_trading_signal(
        message_signal=trading_signal, market_price=market_price
    )

    assert len(convert_price_mock.call_args_list) == 6
    for i, arg in enumerate(args):
        assert convert_price_mock.call_args_list[i][1]["signal_price"] == arg
        assert convert_price_mock.call_args_list[i][1]["market_price"] == market_price
    assert converted_signal == expected_signal


@pytest.mark.parametrize(
    "buy_around, first_target, tick_size, expected_min_max",
    [
        (1.34e-5, 1.375e-5, 1e-8, (1.333e-05, 1.347e-05)),
        (9e-7, 9.4e-7, 1e-8, (8.9e-07, 9.1e-07)),
        (0.06936, 0.0694, 1e-6, (0.069352, 0.069368)),
    ],
)
def test_compute_buy_min_max(buy_around, first_target, tick_size, expected_min_max):
    result_delta = compute_buy_min_max(
        buy_around=buy_around, first_target=first_target, tick_size=tick_size
    )
    assert result_delta == expected_min_max
    assert result_delta[0] < result_delta[1]
