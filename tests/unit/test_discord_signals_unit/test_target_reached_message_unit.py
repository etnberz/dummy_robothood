from robothood.discord_signals.signals import TargetReachedSignal


def test_read_message(mocker, target_reached_message):
    mock_signal_regex = mocker.patch(
        "robothood.discord_signals.target_reached_message.signal_regex",
        side_effect=("ADA", "USDT", "1"),
    )
    target_reached_signal = target_reached_message.read_message()

    assert isinstance(target_reached_signal, TargetReachedSignal)

    assert len(mock_signal_regex.call_args_list) == 3

    assert mock_signal_regex.call_args_list[0][1]["signal"] == "content"
    assert mock_signal_regex.call_args_list[0][1]["pattern"] == r"#([^/]+)(?:/BTC|/USDT|USDT|BTC)"
    assert mock_signal_regex.call_args_list[1][1]["signal"] == "content"
    assert mock_signal_regex.call_args_list[1][1]["pattern"] == r"(?:#ADA)([^/]+)"
    assert mock_signal_regex.call_args_list[2][1]["signal"] == "content"
    assert mock_signal_regex.call_args_list[2][1]["pattern"] == r"\d+(?=st|nd|rd|th)"
