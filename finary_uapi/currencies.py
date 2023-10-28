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
def get_cryptocurrency_by_code(session: requests.Session, code: str):
    currencies = get_currencies(session, "crypto", code)
    if len(currencies["result"]) > 0:
        currency = currencies["result"][0]
        for currency in currencies["result"]:
            if currency["code"] == code:
                return currency
        return currency
    return {}


def get_display_currency_code(session: requests.Session):
    url = f"{API_ROOT}/users/me"
    x = session.get(url)
    display_currency_code = x.json()
    return display_currency_code["result"]["ui_configuration"]["display_currency"][
        "code"
    ]


def update_display_currency_by_code(session: requests.Session, code: str):
    """
    code = ISO 4217 three-letter code
    Currently limited by Finary to "EUR", "USD", "SGD", "CHF", "GBP",or "CAD"
    """ 
    url = f"{API_ROOT}/users/me"
    data = {"ui_configuration": {"display_currency": {"code": code}}}
    data_json = json.dumps(data)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.put(url, data=data_json, headers=headers)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()
