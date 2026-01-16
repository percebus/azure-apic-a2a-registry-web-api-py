"""Configurable mixin for shared components."""

from abc import ABC
from dataclasses import dataclass, field
from logging import Logger

from a2a_registry.config.configuration import Configuration
from a2a_registry.config.os_environ.settings import Settings


@dataclass
class ConfigurableMixin(ABC):
    """Mixin class to provide configuration and settings access."""

    configuration: Configuration = field()

    @property
    def settings(self) -> Settings:
        """Returns the Settings from the configuration."""
        return self.configuration.settings

    @property
    def logger(self) -> Logger:
        """Returns the instnace of the Logger."""
        return self.configuration.logging.logger
