"""Main entrypoint."""

from logging import Logger

from lagom import Container

from a2a_registry.config.os_environ.settings import Settings
from a2a_registry.dependency_injection.container import container
from a2a_registry.services.a2a.protocol import A2AServiceProtocol
from a2a_registry.web.app import flask_api


def run(ctr: Container) -> None:
    """Run the application."""
    logger = ctr[Logger]
    logger.info("Running app")

    a2a_service = ctr[A2AServiceProtocol]
    a2a_service.download_cards()

    logger.info("Running Flask WebAPI")
    settings = ctr[Settings]
    flask_api.run(host="0.0.0.0", port=8000, debug=settings.debug)


def main() -> None:
    """Run the main entry point."""
    run(container)


if __name__ == "__main__":
    main()
