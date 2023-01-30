import pytest

from robothood.discord_signals.signals import TargetReachedSignal
from robothood.discord_signals.target_reached_message import TargetReachedMessage


@pytest.mark.parametrize(
    "content, timestamp, expected_target_signal",
    [
        (
            "TARGET HIT 1st target reached for #DATABTC",
            "2022-01-09",
            TargetReachedSignal(
                timestamp="2022-01-09",
                pair="DATABTC",
                target_num="1",
            ),
        ),
        (
            "TARGET HIT 4th target reached for #LTCUSDT",
            "2018-11-26",
            TargetReachedSignal(
                timestamp="2018-11-26",
                pair="LTCUSDT",
                target_num="4",
            ),
        ),
    ],
)
def test_read_target_message(content, timestamp, expected_target_signal):
    message = TargetReachedMessage(
        response={
            "content": content,
            "timestamp": timestamp,
        }
    )
    assert message.read_message() == expected_target_signal
