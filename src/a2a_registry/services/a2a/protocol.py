"""A2A Service Protocol."""

from typing import Protocol


class A2AServiceProtocol(Protocol):
    """A2AServiceProtocol class."""

    def download_cards(self) -> None:
        """download_cards method."""
        ...
