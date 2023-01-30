import pytest

from robothood.discord_signals.constants import (
    BUY_KEYWORDS,
    PAIR_KEYWORDS,
    SELL_KEYWORDS,
    STOP_KEYWORDS,
)
from robothood.discord_signals.utils import pick_line, signal_regex
from robothood.errors import NoMatchFoundError

INVALID_TRADING_SIGNAL = "invalid"
VALID_BTC_TRADING_SIGNAL = (
    "PAIR: FRONT/BTC \n BUY PRICE: 1340 \n SELLING TARGETS: 1375|1435|1550|1700"
    " \n STOP PRICE: 980"
)
VALID_USDT_TRADING_SIGNAL = (
    "PAIR: LTC/USDT \n BUY PRICE: 61.26 \n SELLING TARGETS: 61.90|65.00|69.00|72.00"
    " \n STOP PRICE: 40.00"
)

VALID_TARGET_REACHED_SIGNAL = ("TARGET HIT 1st target reached for #DATABTC",)

INVALID_TRADING_SIGNAL_LIST = [el for el in INVALID_TRADING_SIGNAL.split("\n") if el != ""]
VALID_BTC_TRADING_SIGNAL_LIST = [el for el in VALID_BTC_TRADING_SIGNAL.split("\n") if el != ""]
VALID_USDT_TRADING_SIGNAL_LIST = [el for el in VALID_USDT_TRADING_SIGNAL.split("\n") if el != ""]


@pytest.mark.parametrize(
    "signal_list, keywords, raises",
    [
        (INVALID_TRADING_SIGNAL_LIST, BUY_KEYWORDS, True),
        (VALID_BTC_TRADING_SIGNAL_LIST, BUY_KEYWORDS, False),
        (VALID_BTC_TRADING_SIGNAL_LIST, PAIR_KEYWORDS, False),
        (VALID_BTC_TRADING_SIGNAL_LIST, SELL_KEYWORDS, False),
        (VALID_BTC_TRADING_SIGNAL_LIST, STOP_KEYWORDS, False),
        (VALID_BTC_TRADING_SIGNAL_LIST, ["Le cuisinier secoue les nouilles"], True),
        (VALID_USDT_TRADING_SIGNAL_LIST, BUY_KEYWORDS, False),
        (VALID_USDT_TRADING_SIGNAL_LIST, PAIR_KEYWORDS, False),
        (VALID_USDT_TRADING_SIGNAL_LIST, SELL_KEYWORDS, False),
        (VALID_USDT_TRADING_SIGNAL_LIST, STOP_KEYWORDS, False),
        (VALID_USDT_TRADING_SIGNAL_LIST, ["Le cuisinier secoue les nouilles"], True),
    ],
)
def test_pick_lines_raises(signal_list, keywords, raises):
    if not raises:
        pick_line(signal_list=signal_list, keywords=keywords)
    else:
        err_mess = f"Signal {signal_list} does not contain all of the keywords: {keywords}"
        with pytest.raises(NoMatchFoundError) as exception:
            pick_line(signal_list=signal_list, keywords=keywords)
            assert str(exception.value) == err_mess


@pytest.mark.parametrize(
    "signal_list, keywords, expected_result",
    [
        (VALID_BTC_TRADING_SIGNAL_LIST, PAIR_KEYWORDS, "PAIR: FRONT/BTC "),
        (VALID_BTC_TRADING_SIGNAL_LIST, BUY_KEYWORDS, " BUY PRICE: 1340 "),
        (
            VALID_BTC_TRADING_SIGNAL_LIST,
            SELL_KEYWORDS,
            " SELLING TARGETS: 1375|1435|1550|1700 ",
        ),
        (VALID_BTC_TRADING_SIGNAL_LIST, STOP_KEYWORDS, " STOP PRICE: 980"),
        (VALID_USDT_TRADING_SIGNAL_LIST, PAIR_KEYWORDS, "PAIR: LTC/USDT "),
        (VALID_USDT_TRADING_SIGNAL_LIST, BUY_KEYWORDS, " BUY PRICE: 61.26 "),
        (
            VALID_USDT_TRADING_SIGNAL_LIST,
            SELL_KEYWORDS,
            " SELLING TARGETS: 61.90|65.00|69.00|72.00 ",
        ),
        (VALID_USDT_TRADING_SIGNAL_LIST, STOP_KEYWORDS, " STOP PRICE: 40.00"),
    ],
)
def test_pick_lines_results(signal_list, keywords, expected_result):
    assert pick_line(signal_list=signal_list, keywords=keywords) == expected_result


@pytest.mark.parametrize(
    "signal, pattern, raises",
    [
        ("FRONT/BTC", r"PAIR: ([\w.-]+)", True),
        ("PAIR: FRONT/BTC", r"PAIR: ([\w.-]+)", False),
        ("BUY PRICE:", r"(\d+(?:\.\d+)?)", True),
        ("BUY PRICE: 1340", r"(\d+(?:\.\d+)?)", False),
        ("SELLING TARGETS: 1375|1435|1550|1700", r"(\d+(?:\.\d+)?)", False),
        ("STOP PRICE: 980", r"(\d+(?:\.\d+)?)", False),
        ("LTC/USDT", r"PAIR: ([\w.-]+)", True),
        ("PAIR: LTC/USDT", r"PAIR: ([\w.-]+)", False),
        ("BUY PRICE", r"(\d+(?:\.\d+)?)", True),
        ("BUY PRICE: 61.26", r"(\d+(?:\.\d+)?)", False),
        ("SELLING TARGETS: 61.90|65.00|69.00|72.00", r"(\d+(?:\.\d+)?)", False),
        ("STOP PRICE: 40.00", r"(\d+(?:\.\d+)?)", False),
        ("TARGET HIT 1st target reached for #DATABTC", r"\d+(?=st|nd|rd|th)", False),
        ("TARGET HIT target reached for #DATABTC", r"\d+(?=st|nd|rd|th)", True),
    ],
)
def test_signal_regex_raises(signal, pattern, raises):
    if not raises:
        signal_regex(pattern=pattern, signal=signal)
    else:
        err_mess = f"Pattern {pattern} not found in {signal}"
        with pytest.raises(NoMatchFoundError) as exception:
            signal_regex(pattern=pattern, signal=signal)
            assert str(exception.value) == err_mess


@pytest.mark.parametrize(
    "signal, pattern, expected_result",
    [
        ("PAIR: FRONT/BTC", r"PAIR: ([\w.-]+)", "FRONT"),
        ("PAIR: FRONT/BTC", r"(?:FRONT/)([^/]+)", "BTC"),
        ("BUY PRICE: 1340", r"(\d+(?:\.\d+)?)", "1340"),
        (
            "SELLING TARGETS: 1375|1435|1550|1700",
            r"(\d+(?:\.\d+)?)",
            ["1375", "1435", "1550", "1700"],
        ),
        ("STOP PRICE: 980", r"(\d+(?:\.\d+)?)", "980"),
        ("PAIR: LTC/USDT", r"PAIR: ([\w.-]+)", "LTC"),
        ("PAIR: LTC/USDT", r"(?:LTC/)([^/]+)", "USDT"),
        ("BUY PRICE: 61.26", r"(\d+(?:\.\d+)?)", "61.26"),
        (
            "SELLING TARGETS: 61.90|65.00|69.00|72.00",
            r"(\d+(?:\.\d+)?)",
            ["61.90", "65.00", "69.00", "72.00"],
        ),
        ("STOP PRICE: 40.00", r"(\d+(?:\.\d+)?)", "40.00"),
        ("TARGET HIT 1st target reached for #DATABTC", r"\d+(?=st|nd|rd|th)", "1"),
        ("1 2nd 89 5211 45645 3rd greg 4th", r"\d+(?=st|nd|rd|th)", ["2", "3", "4"]),
    ],
)
def test_signal_regex_results(signal, pattern, expected_result):
    assert signal_regex(pattern=pattern, signal=signal) == expected_result
