import pytest

from robothood.discord_signals.signals import TradingSignal
from robothood.discord_signals.trading_message import TradingMessage


@pytest.mark.parametrize(
    "content, timestamp, expected_trading_signal",
    [
        (
            "PAIR: FRONT/BTC \n BUY PRICE: 1340 \n SELLING TARGETS: 1375|1435|1550|1700"
            " \n STOP PRICE: 980",
            "2022-02-02",
            TradingSignal(
                timestamp="2022-02-02",
                quote_currency="FRONT",
                base_currency="BTC",
                buy_around="1340",
                targets=["1375", "1435", "1550", "1700"],
                stop_loss="980",
            ),
        ),
        (
            "PAIR: LTC/USDT \n BUY PRICE: 61.26 \n SELLING TARGETS: 61.90|65.00|69.00|72.00"
            " \n STOP PRICE: 40.00",
            "2021-03-24",
            TradingSignal(
                timestamp="2021-03-24",
                quote_currency="LTC",
                base_currency="USDT",
                buy_around="61.26",
                targets=["61.90", "65.00", "69.00", "72.00"],
                stop_loss="40.00",
            ),
        ),
    ],
)
def test_read_trading_message(content, timestamp, expected_trading_signal):
    message = TradingMessage(
        response={
            "content": content,
            "timestamp": timestamp,
        }
    )

    signal = message.read_message()

    assert signal == expected_trading_signal
