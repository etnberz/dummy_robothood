from robothood.discord_signals.constants import REGEX_PATTERNS
from robothood.discord_signals.signals import TradingSignal


def test_read_message(mocker, trading_message):
    mock_pick_line = mocker.patch(
        "robothood.discord_signals.trading_message.pick_line", return_value="scooby"
    )
    mock_signal_regex = mocker.patch(
        "robothood.discord_signals.trading_message.signal_regex",
        side_effect=["doo", "12", ["16", "2", "4", "9"], "6", "T"],
    )
    trading_signal = trading_message.read_message()

    assert isinstance(trading_signal, TradingSignal)

    assert len(mock_pick_line.call_args_list) == 5
    for i, k in enumerate(REGEX_PATTERNS.keys()):
        assert mock_pick_line.call_args_list[i][1]["signal_list"] == ["content"]
        assert mock_pick_line.call_args_list[i][1]["keywords"] == REGEX_PATTERNS[k]["keywords"]
    assert mock_pick_line.call_args_list[4][1]["signal_list"] == ["content"]
    assert mock_pick_line.call_args_list[4][1]["keywords"] == ["pair"]

    assert len(mock_signal_regex.call_args_list) == 5
    for i, k in enumerate(REGEX_PATTERNS.keys()):
        assert mock_signal_regex.call_args_list[i][1]["signal"] == "scooby"
        assert mock_signal_regex.call_args_list[i][1]["pattern"] == REGEX_PATTERNS[k]["pattern"]
    assert mock_signal_regex.call_args_list[4][1]["signal"] == "scooby"
    assert mock_signal_regex.call_args_list[4][1]["pattern"] == "(?:PAIR: doo/)([^/]+)"
