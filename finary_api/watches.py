import logging
import requests
import json
from .constants import API_ROOT


def get_watches(session: requests.Session, query: str):
    """
    This function will get a list of watches to be added,
    a user watch can be added as a generic asset
    """
    url = f"{API_ROOT}/watches/autocomplete"
    params = {}
    if query:
        params["query"] = query

    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()
