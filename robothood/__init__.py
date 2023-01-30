"""Generous Crypto Trading Bot"""
# pylint: disable=unused-variable

import json
import logging.config
import os
from logging import LogRecord
from pathlib import Path

LOG_CONFIG_PATH = (Path(__file__).parent / "config/log_config.json").resolve(strict=True)

LOG_FILES_PATH = Path(os.environ["ROBOTHOOD_PATH"]) / "logs"


class RobotHoodLogFilter(logging.Filter):  # pylint:disable=too-few-public-methods
    """Log filter to only keep robothood logs"""

    def filter(self, record: LogRecord) -> bool:
        """Filter log records that doesn't contain robothood in their name

        Parameters
        ----------
        record: LogRecord
            The log record

        Returns
        -------
        bool
            The filter
        """
        return not record.name.startswith("discord.")


if not os.path.isdir(LOG_FILES_PATH):
    os.mkdir(LOG_FILES_PATH)
LOG_FILES_PATH = LOG_FILES_PATH / "robothood.log"

with LOG_CONFIG_PATH.open(mode="r") as log_config_file:
    config_dict = json.load(log_config_file)
    config_dict["filters"]["robothoodlogfilter"]["()"] = RobotHoodLogFilter
    config_dict["handlers"]["file"]["filename"] = LOG_FILES_PATH
    logging.config.dictConfig(config_dict)

logger = logging.getLogger(__name__)
logger.info("Logging configured with %s", str(LOG_CONFIG_PATH))
VERSION = "0.7.0"
