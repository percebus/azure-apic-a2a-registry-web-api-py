"""Initializer Service."""

import json
import os
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import requests
import uritemplate
from azure.mgmt.apicenter.models import Api

from a2a_registry.config.mixin import ConfigurableMixin
from a2a_registry.services.a2a.protocol import A2AServiceProtocol

if TYPE_CHECKING:
    from azure.core.credentials import AccessToken
    from azure.mgmt.apicenter._serialization import JSON


@dataclass
class A2AService(A2AServiceProtocol, ConfigurableMixin):
    """InitializerService class."""

    apis: Iterable[Api] = field()

    uri_template: str = field(
        default="https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.ApiCenter/services/{service_name}/workspaces/{workspace_name}/apis/{api_name}?api-version={api_version}"
    )

    def download_cards(self) -> None:
        """download_cards method."""
        # TODO? move this to DI?
        # fmt: off
        a2a_apis = (
            api
            for api in self.apis
            if str(api.properties.kind).upper() == 'A2A'  # pyright: ignore[reportOptionalMemberAccess] # FIXME? kind is str | ApiKind
        )
        # fmt: on

        access_token: AccessToken = self.configuration.get_token()
        headers = {"Authorization": f"Bearer {access_token.token}", "Content-Type": "application/json"}

        api_center_dict = self.settings.apic.model_dump()

        self.logger.info("Listing APIs")
        for a2a_api in a2a_apis:
            self.logger.info("Api.id: %s", a2a_api.id)
            self.logger.info("Api.name: %s", a2a_api.name)
            self.logger.info("Api.type: %s", a2a_api.type)

            properties: JSON = a2a_api.properties.as_dict()  # pyright: ignore[reportOptionalMemberAccess] # FIXME
            self.logger.debug(properties)

            _api_center_dict = api_center_dict.copy()
            _api_center_dict["api_name"] = a2a_api.name
            uri = uritemplate.expand(self.uri_template, _api_center_dict)
            self.logger.info("Fetching data from %s", uri)

            response = requests.get(uri, headers=headers, timeout=15)
            response.raise_for_status()
            api_data = response.json()
            agent_card = api_data["properties"]["agentCard"]

            # TODO move to config
            output_folder = "tmp/a2a"
            os.makedirs(output_folder, exist_ok=True)

            output_file_path: str = f"{output_folder}/{a2a_api.name}.json"
            if os.path.isfile(output_file_path):
                os.remove(output_file_path)

            with open(f"tmp/a2a/{a2a_api.name}.json", "w") as output_file:
                json.dump(agent_card, output_file, indent=4)

            self.logger.debug(api_data)
