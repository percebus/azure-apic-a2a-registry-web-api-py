"""Dependency Injection container."""

from collections.abc import Iterable
from logging import Logger

from azure.core.credentials import TokenCredential
from azure.identity import DefaultAzureCredential
from azure.mgmt.apicenter import ApiCenterMgmtClient
from azure.mgmt.apicenter.models import Api
from dotenv import load_dotenv
from lagom import Container

from a2a_registry.config.configuration import Configuration
from a2a_registry.config.logs import LoggingConfig
from a2a_registry.config.os_environ.api_center import ApiCenterSettings
from a2a_registry.config.os_environ.settings import Settings
from a2a_registry.services.a2a.protocol import A2AServiceProtocol
from a2a_registry.services.a2a.service import A2AService


def create_settings(ctr: ReadableContainer) -> Settings:
    load_dotenv()  # FIXME? move to main.py?
    settings = Settings()  # pyright: ignore[reportCallIssue]

    # return Singleton(settings) # TODO
    return settings


container = Container()

container[LoggingConfig] = LoggingConfig
container[Logger] = lambda c: c[LoggingConfig].logger

container[Settings] = create_settings
container[ApiCenterSettings] = lambda c: c[Settings].apic

container[DefaultAzureCredential] = DefaultAzureCredential
container[TokenCredential] = lambda c: c[DefaultAzureCredential]

# fmt: off
container[Configuration] = lambda c: Configuration(
    logging=c[LoggingConfig],
    settings=c[Settings],
    credential=c[TokenCredential],
)
# fmt: on


# fmt: off
container[ApiCenterMgmtClient] = lambda c: ApiCenterMgmtClient(
    credential=c[TokenCredential],
    subscription_id=c[ApiCenterSettings].subscription_id,
)
# fmt: on

# fmt: off
container[Iterable[Api]] = lambda c: c[ApiCenterMgmtClient].apis.list(
    resource_group_name=c[ApiCenterSettings].resource_group_name,
    service_name=c[ApiCenterSettings].service_name,
    workspace_name=c[ApiCenterSettings].workspace_name,
    # filter="$properties.kind eq 'a2a'",  # FIXME
)
# fmt: on

container[A2AService] = lambda c: A2AService(
    configuration=c[Configuration],
    apis=c[Iterable[Api]],
)

container[A2AServiceProtocol] = lambda c: c[A2AService]
