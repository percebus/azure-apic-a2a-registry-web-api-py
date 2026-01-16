"""API Center Settings."""

from pydantic import BaseModel, Field


class ApiCenterSettings(BaseModel):
    """ApiCenterSettings class."""

    subscription_id: str = Field()

    resource_group_name: str = Field()

    service_name: str = Field()

    workspace_name: str = Field(default="default")

    api_version: str = Field(default="2023-07-01-preview")
