""".env os.environ ENVIRONMENT VARIABLES settings module."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from a2a_registry.config.os_environ.api_center import ApiCenterSettings


class Settings(BaseSettings):
    """Base class for settings."""

    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False,
        env_prefix="",
        env_nested_delimiter="__",
    )

    debug: bool = Field(default=False)
    dry_run: bool = Field(default=True)
    environment: str = Field(min_length=2)

    apic: ApiCenterSettings = Field()
