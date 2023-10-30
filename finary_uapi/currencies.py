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


# utils functions


def get_currency_by_code(session: requests.Session, type: str, code: str):
    """
    type = 'crypto' or 'fiat'
    """
    currencies = get_currencies(session, type, code)
    if len(currencies["result"]) > 0:
        currency = currencies["result"][0]
        for currency in currencies["result"]:
            if currency["code"] == code:
                return currency
        return currency
    return {}


def get_cryptocurrency_by_code(session: requests.Session, code: str):
    return get_currency_by_code(session, "crypto", code)


def get_fiatcurrency_by_code(session: requests.Session, code: str):
    return get_currency_by_code(session, "fiat", code)
