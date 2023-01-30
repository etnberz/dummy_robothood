import datetime
from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest

from robothood.discord_bot.constants import TS_CHANNEL_ID, TS_GUILD_ID
from robothood.discord_bot.discord_bot import DiscordBot
from robothood.discord_signals.signals import TargetReachedSignal, TradingSignal
from robothood.discord_signals.target_reached_message import TargetReachedMessage
from robothood.discord_signals.trading_message import TradingMessage
from tests.conftest import TestClient, mock_trading_signal_manager  # pylint:disable=import-error


@pytest.fixture()
def discord_bot():
    return DiscordBot(guild_id=TS_GUILD_ID, channel_id=TS_CHANNEL_ID)


@pytest.mark.parametrize(
    "content, time_stamp, message_type",
    [
        ("yo", datetime.datetime(2022, 11, 22, 13, 36, 36), None),
        (
            "PAIR: FRONT/BTC \n BUY PRICE: 1340 \n SELLING TARGETS: 1375|1435|1550|1700"
            " \n STOP PRICE: 980",
            datetime.datetime(2021, 6, 14, 7, 24, 2),
            TradingMessage,
        ),
        (
            "TARGET HIT 1st target reached for #DATABTC",
            datetime.datetime(2022, 11, 22, 13, 36, 36),
            TargetReachedMessage,
        ),
        (
            "PAIR: LTC/USDT \n BUY PRICE: 61.26 \n SELLING TARGETS: 61.90|65.00|69.00|72.00"
            " \n STOP PRICE: 40.00",
            datetime.datetime(2021, 6, 14, 7, 24, 2),
            TradingMessage,
        ),
        (
            "TARGET HIT 4th target reached for #LTCUSDT",
            datetime.datetime(2022, 11, 22, 13, 36, 36),
            TargetReachedMessage,
        ),
    ],
)
def test_process_message(monkeypatch, discord_bot, content, time_stamp, message_type):

    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.utcnow.return_value = time_stamp
    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    time_stamp = time_stamp.strftime("%Y-%m-%d %H:%M:%S")

    res = discord_bot.process_message(message_content=content)
    datetime_mock.utcnow.assert_called_once()

    if message_type is None:
        assert res is None
    else:
        expected_message = message_type(response={"timestamp": time_stamp, "content": content})
        assert res == expected_message


@dataclass
class ChannelOrGuildTestClass:
    id: int


@dataclass
class MessageTestClass:
    guild: ChannelOrGuildTestClass
    channel: ChannelOrGuildTestClass
    content: str


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "guild_id, channel_id, ids_ok, message_content, processed_message, message_type, signal",
    [
        (TS_GUILD_ID, TS_CHANNEL_ID, True, "Hi", None, "none", None),
        (TS_GUILD_ID, 1, False, "Hi", None, "none", None),
        (1, TS_CHANNEL_ID, False, "Hi", None, "none", None),
        (
            TS_GUILD_ID,
            TS_CHANNEL_ID,
            True,
            "Hi",
            TradingMessage(
                response={
                    "content": "Hi",
                    "timestamp": "2020-01-02",
                }
            ),
            "trading",
            TradingSignal(
                timestamp="2020-11-01 13:00",
                quote_currency="KAVA",
                base_currency="USDT",
                buy_around="0.837",
                targets=["0.845", "0.876", "0.950", "0.990"],
                stop_loss="0.6800",
            ),
        ),
        (
            TS_GUILD_ID,
            TS_CHANNEL_ID,
            True,
            "Hi",
            TargetReachedMessage(
                response={
                    "content": "Hi",
                    "timestamp": "2020-01-02",
                }
            ),
            "target",
            TargetReachedSignal(
                timestamp="2020-11-01 13:00",
                pair="ETHBTC",
                target_num="1",
            ),
        ),
    ],
    ids=[
        "None Message",
        "Wrong Channel ID",
        "Wrong Guild ID",
        "Trading Message",
        "Target Message",
    ],
)
async def test_on_message(
    mocker,
    discord_bot,
    guild_id,
    ids_ok,
    channel_id,
    message_content,
    processed_message,
    message_type,
    signal,
):
    message = MessageTestClass(
        guild=ChannelOrGuildTestClass(id=guild_id),
        channel=ChannelOrGuildTestClass(id=channel_id),
        content=message_content,
    )

    mocker.patch(
        "robothood.signal_managers.signal_manager.Client",
        return_value=TestClient(),
    )

    mock_process_message = mocker.patch(
        "robothood.discord_bot.discord_bot.DiscordBot.process_message",
        return_value=processed_message,
    )
    mock_read_message_trading = mocker.patch(
        "robothood.discord_signals.trading_message.TradingMessage.read_message",
        return_value=signal,
    )
    mock_read_message_target = mocker.patch(
        "robothood.discord_signals.target_reached_message.TargetReachedMessage.read_message",
        return_value=signal,
    )
    mock_trading_signal_manager(mocker, trading_signal=signal)

    mock_trading_manager_process_signal = mocker.patch(
        "robothood.signal_managers.trading_signal_manager.TradingSignalManager.process_signal"
    )
    mock_target_manager_process_signal = mocker.patch(
        "robothood.signal_managers.target_reached_signal_manager.TargetReachedSignalManager"
        ".process_signal"
    )

    await discord_bot.on_message(message)

    if ids_ok:
        mock_process_message.assert_called_once_with(message_content=message_content)
        if message_type == "none":
            mock_read_message_target.assert_not_called()
            mock_target_manager_process_signal.assert_not_called()
            mock_read_message_trading.assert_not_called()
            mock_trading_manager_process_signal.assert_not_called()
    else:
        mock_process_message.assert_not_called()

    if message_type == "trading":
        mock_read_message_trading.assert_called_once()
        mock_trading_manager_process_signal.assert_called_once()
        mock_read_message_target.assert_not_called()
        mock_target_manager_process_signal.assert_not_called()

    if message_type == "target":
        mock_read_message_target.assert_called_once()
        mock_target_manager_process_signal.assert_called_once()
        mock_read_message_trading.assert_not_called()
        mock_trading_manager_process_signal.assert_not_called()
