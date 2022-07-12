import logging
import requests
import json
from .constants import API_ROOT


def get_scpis(session: requests.Session, query: str):
    """
    This function will get a list of scpis to be added,
    and not the user scpis, see user_scpis for the scpis owned by the user
    """
    url = f"{API_ROOT}/scpis/autocomplete"
    params = {}
    if query:
        params["query"] = query

    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()
