"""Logging configuration for the application."""

import logging
import logging.config
from dataclasses import dataclass, field
from logging import Logger


@dataclass
class LoggingConfig:
    """Logging Configuration class."""

    name: str = field(default="a2a_registry")

    config_path: str = field(default="config/logging.conf")

    @property
    def logger(self) -> Logger:
        """Get the logger instance for this configuration."""
        return logging.getLogger(self.name)

    def __post_init__(self) -> None:
        """Post-initialization to set up logging configuration."""
        logging.config.fileConfig(self.config_path)
        self.logger.debug("Loaded logging configuration from %s", self.config_path)


def run(logger: Logger) -> None:  # pragma: no cover
    """Runner function."""
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")


def main() -> None:  # pragma: no cover
    """Run the main function."""
    logging_config = LoggingConfig()
    logger: Logger = logging_config.logger

    logger.info("Running main.")
    run(logger)


if __name__ == "__main__":  # pragma: no cover
    main()
