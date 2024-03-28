import json
import logging
import httpx

from .constants import API_ROOT


def get_generic_asset_categories(session: httpx.Client):
    """ """
    url = f"{API_ROOT}/generic_asset_categories/autocomplete"
    x = session.get(url)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()
