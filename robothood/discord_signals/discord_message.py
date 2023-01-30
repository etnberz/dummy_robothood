from abc import ABC
from typing import Any, Dict


class DiscordMessage(ABC):  # pylint:disable=unused-variable
    """Discord Message Class"""

    def __init__(self, response: Dict):
        self.content = response["content"]
        self.timestamp = response["timestamp"]

    def __eq__(self, other: Any) -> bool:
        return all(
            [
                isinstance(other, DiscordMessage),
                self.content == other.content,
                self.timestamp == other.timestamp,
            ]
        )

    def read_message(self) -> Any:
        """Read the message

        Returns
        -------
        Any
            The signal read
        """
