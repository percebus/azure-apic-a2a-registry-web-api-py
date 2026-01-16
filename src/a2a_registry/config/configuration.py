"""Shared Configuration Module."""

from dataclasses import dataclass, field
from typing import Any

from azure.core.credentials import AccessToken, TokenCredential
from azure.identity import DefaultAzureCredential

from a2a_registry.config.logs import LoggingConfig
from a2a_registry.config.os_environ.settings import Settings


@dataclass
class Configuration:
    """Shared configuration model for the application."""

    settings: Settings = field(default_factory=Settings)  # type: ignore[assignment]  # FIXME

    logging: LoggingConfig = field(default_factory=LoggingConfig)

    credential: TokenCredential = field(default_factory=DefaultAzureCredential)

    @property
    def debug(self) -> bool:
        """Return True if the environment is 'dev' or 'test', otherwise False."""
        return self.settings.debug

    def safe_model_dump(self) -> dict[str, Any] | None:
        """Safely dump the model to a dictionary, ignoring any errors."""
        return self.settings.model_dump() if self.debug else None

    def get_token(self) -> AccessToken:
        """Get AccessToken."""
        return self.credential.get_token("https://management.azure.com/.default")
