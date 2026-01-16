"""Kubernetes related models."""

from pydantic import BaseModel, Field


class KubernetesStatus(BaseModel):
    """
    KubernetesStatus class.

    Fields:
        - status: str
    """

    status: str = Field()
