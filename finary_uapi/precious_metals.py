import logging
import httpx
import json
from .constants import API_ROOT


def get_precious_metals(session: httpx.Client, query: str):
    """
    This function will get a list of metals to be added,
    and not the user metals, see views/commodities for the user metals
    """
    url = f"{API_ROOT}/precious_metals/autocomplete"
    params = {}
    if query:
        params["query"] = query

    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()
