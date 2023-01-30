import logging
import os

from robothood.discord_bot.constants import TS_CHANNEL_ID, TS_GUILD_ID
from robothood.discord_bot.discord_bot import DiscordBot
from robothood.hoodapi.hoodapi import create_database
from robothood.hoodapi.peewee_models import DB_PATH

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    if not os.path.isfile(DB_PATH):
        create_database()
        logger.info("DB created at: %s", DB_PATH)

    bot = DiscordBot(guild_id=TS_GUILD_ID, channel_id=TS_CHANNEL_ID)
    bot.run(os.environ["DISCORD_TOKEN"])
