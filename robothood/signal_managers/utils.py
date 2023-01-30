import math
from typing import Tuple

from robothood.discord_signals.signals import TradingSignal

# pylint:disable=unused-variable


def convert_price_message_to_real_price(signal_price: float, market_price: float) -> float:
    """Convert message price which is expressed in a human-readable way to proper base currency price

    Parameters
    ----------
    signal_price: str
        Signal price
    market_price: str
        Market price

    Returns
    -------
    str
        Price converted in BTC

    """
    prices_ratio = signal_price // market_price
    if prices_ratio == 0:
        prices_ratio = 1
    power = int(math.log10(prices_ratio))
    if signal_price * math.pow(10, -power) / market_price > 5:
        power += 1
    return round(signal_price * math.pow(10, -power), 8)


def convert_trading_signal(message_signal: TradingSignal, market_price: float) -> TradingSignal:
    """Convert message signal which is expressed in a human-readable way to proper signal
    usable by Binance

    Parameters
    ----------
    message_signal: str
        Signal received by message with human-readable prices
    market_price: str
        Market price

    Returns
    -------
    TradingSignal
        TradingSignal usable by Binance API

    """
    message_signal.buy_around = convert_price_message_to_real_price(
        signal_price=message_signal.buy_around, market_price=market_price
    )
    message_signal.targets = [
        convert_price_message_to_real_price(signal_price=target, market_price=market_price)
        for target in message_signal.targets
    ]
    message_signal.stop_loss = convert_price_message_to_real_price(
        signal_price=message_signal.stop_loss, market_price=market_price
    )
    return message_signal


def compute_buy_min_max(
    buy_around: float, first_target: float, tick_size: float
) -> Tuple[float, float]:
    """Compute min and max buying prices

    Parameters
    ----------
    buy_around: float
        The price to buy around according to trading signal
    first_target: float
        The first price target of the trading signal
    tick_size: float
        The tick size of the considered crypto currency

    Returns
    -------
    Tuple[float, float]
        Min and max buying prices
    """

    digits = math.floor(math.log(tick_size, 10))
    digits = digits * (-1) if digits < 0 else digits
    delta = 0.2 * (first_target - buy_around)
    return round(buy_around - delta, digits), round(buy_around + delta, digits)
