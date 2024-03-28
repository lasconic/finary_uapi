import logging
from .constants import API_ROOT
import httpx
import json


def get_institutions(session: httpx.Client, name: str):
    """
    name
    """
    url = f"{API_ROOT}/users/me/institutions/autocomplete"
    params = {}
    if name:
        params["name"] = name

    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()
