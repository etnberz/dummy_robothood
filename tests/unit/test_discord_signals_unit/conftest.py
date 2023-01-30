import pytest

from robothood.discord_signals.target_reached_message import TargetReachedMessage
from robothood.discord_signals.trading_message import TradingMessage


@pytest.fixture()
def response_fixture():
    return {
        "guild_id": "1",
        "channel_id": "1",
        "author": {
            "username": "robert",
            "discriminator": "13",
        },
        "content": "content",
        "timestamp": "2022-02-02",
    }


@pytest.fixture()
def trading_message(response_fixture):
    return TradingMessage(response=response_fixture)


@pytest.fixture()
def target_reached_message(response_fixture):
    return TargetReachedMessage(response=response_fixture)
