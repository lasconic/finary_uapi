import logging
from .constants import API_ROOT
import requests
import json


def get_currencies(session: requests.Session, type: str, query: str):
    """
    type = 'crypto' or 'fiat'
    """
    url = f"{API_ROOT}/currencies/autocomplete"
    params = {}
    if type:
        params["type"] = type
    if query:
        params["query"] = query

    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def get_cryptocurrency_by_code(session: requests.Session, code: str):
    currencies = get_currencies(session, "crypto", code)
    if len(currencies["result"]) > 0:
        currency = currencies["result"][0]
        for currency in currencies["result"]:
            if currency["code"] == code:
                return currency
        return currency
    return {}
