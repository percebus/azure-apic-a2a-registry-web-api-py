"""
/health endpoints for Kubernetes liveness and readiness probes.

Endpoints:
    - /health/ready
    - /health/live
"""

import logging

from flask import Blueprint

from a2a_registry.models.kubernetes.status import KubernetesStatus
from a2a_registry.typing.json import SerializedJson

blueprint = Blueprint("health", __name__, url_prefix="/health")
logger = logging.getLogger(__name__)


@blueprint.route("/ready")
def is_ready() -> SerializedJson:
    """
    is_ready(): Determines if the service is ready to accept requests.

    Returns
    -------
        A KubernetesStatus in a Json format.
    """
    logging.info("is_ready is invoked")
    payload = KubernetesStatus(**{"status": "Ready!"})

    response: SerializedJson = payload.model_dump_json()
    logger.debug("is_ready response: %s", response)
    return response


@blueprint.route("/live")
def is_live() -> SerializedJson:
    """
    is_live(): Determines if the service is alive.

    Returns
    -------
        A KubernetesStatus in a Json format.
    """
    logging.info("is_live is invoked")
    payload = KubernetesStatus(**{"status": "Still alive!"})

    response: SerializedJson = payload.model_dump_json()
    logger.debug("is_live response: %s", response)
    return response
