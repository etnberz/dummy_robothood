import datetime
import logging
from typing import Any, Optional, Union

import discord  # pylint:disable=import-error

from robothood.discord_signals.constants import SIGNAL_KEYWORDS, TARGET_REACH_KEYWORDS
from robothood.discord_signals.signals import TargetReachedSignal, TradingSignal
from robothood.discord_signals.target_reached_message import TargetReachedMessage
from robothood.discord_signals.trading_message import TradingMessage
from robothood.signal_managers.target_reached_signal_manager import TargetReachedSignalManager
from robothood.signal_managers.trading_signal_manager import TradingSignalManager

logger = logging.getLogger(__name__)


class DiscordBot(discord.Client):  # type: ignore
    """Discord Listener Class"""

    def __init__(self, guild_id: int, channel_id: int) -> None:
        super(DiscordBot, self).__init__()
        self.guild_id = guild_id
        self.channel_id = channel_id

    @staticmethod
    def process_message(
        message_content: str,
    ) -> Optional[Union[TradingMessage, TargetReachedMessage]]:
        """Process the message and returns the adequate type of message or none if the message
        content is not interesting.

        Returns
        -------
        Optional[Union[TradingMessage, TargetReachedMessage]]
            The message issued from the response
        """
        logger.info("Message Received")
        logger.info("Processing Message...")
        response = {
            "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "content": message_content,
        }
        if all([el in message_content.lower() for el in SIGNAL_KEYWORDS]):
            logger.info("This is a trading message")
            return TradingMessage(response=response)
        if all([el in message_content.lower() for el in TARGET_REACH_KEYWORDS]):
            logger.info("This is a target reached message")
            return TargetReachedMessage(response=response)
        logger.info("This is not an interesting message")
        return None

    async def on_ready(self) -> None:
        """Log when the bot is ready to run"""
        logger.info("Logged in as %s", self.user)

    async def on_message(self, message: Any) -> None:
        """Listen to Discord Websocket Gateway

        Parameters
        ----------
        message: Any
            Websocket Response
        """

        if message.guild.id == self.guild_id and message.channel.id == self.channel_id:
            processed_message = self.process_message(message_content=message.content)
            if processed_message is not None:
                signal = processed_message.read_message()
                logger.info("%s", signal)
                if isinstance(signal, TradingSignal):
                    trading_manager = TradingSignalManager(signal=signal)
                    trading_manager.process_signal()
                elif isinstance(signal, TargetReachedSignal):
                    target_manager = TargetReachedSignalManager(signal=signal)
                    target_manager.process_signal()
