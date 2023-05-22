import logging
from .constants import API_ROOT
import requests
import json


def get_institutions(session: requests.Session, name: str):
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
