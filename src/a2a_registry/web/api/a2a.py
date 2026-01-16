"""A2A API."""

import logging
import os
from typing import TYPE_CHECKING

from flask import Blueprint, Response, json, jsonify

if TYPE_CHECKING:
    from a2a_registry.typing.json import JsonObject

blueprint = Blueprint("a2a", __name__, url_prefix="/api/a2a")
logger = logging.getLogger(__name__)


@blueprint.route("/", methods=["GET"])
async def post_async() -> Response:
    """/list a2a registry."""
    a2a_cards_folder = "tmp/a2a"

    # fmt: off
    a2a_cards_paths: list[str] = [
        os.path.join(a2a_cards_folder, file_name)
        for file_name in os.listdir(a2a_cards_folder)
        if file_name.endswith('.json')]
    # fmt: on

    a2a_cards: list[JsonObject] = []
    for a2a_card_path in a2a_cards_paths:
        logger.info("Opening %s", a2a_card_path)
        with open(a2a_card_path) as a2a_card_file:
            a2a_card_json = json.load(a2a_card_file)
            logger.debug(a2a_card_json)
            a2a_cards.append(a2a_card_json)

    return jsonify(a2a_cards)
