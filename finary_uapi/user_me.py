import json
import logging
import httpx
from typing import Any

from .utils import get_and_print
from .constants import API_ROOT


def get_user_me(session: httpx.Client) -> Any:
    url = f"{API_ROOT}/users/me"
    return get_and_print(session, url)


def get_user_me_institution_connections(session: httpx.Client) -> Any:
    url = f"{API_ROOT}/users/me/institution_connections/details"
    return get_and_print(session, url)


def get_user_me_sharing_links(session: httpx.Client) -> Any:
    url = f"{API_ROOT}/users/me/sharing_links"
    return get_and_print(session, url)


def get_user_me_organizations(session: httpx.Client) -> Any:
    url = f"{API_ROOT}/users/me/organizations"
    return get_and_print(session, url)


def get_user_me_subscription_details(session: httpx.Client) -> Any:
    url = f"{API_ROOT}/users/me/subscription_details"
    return get_and_print(session, url)


# convenience functions


def get_display_currency_code(session: httpx.Client):
    display_currency_code = get_user_me(session)
    return display_currency_code["result"]["ui_configuration"]["display_currency"][
        "code"
    ]


def update_display_currency_by_code(session: httpx.Client, code: str):
    """
    code = ISO 4217 three-letter code
    Currently limited by Finary to "EUR", "USD", "SGD", "CHF", "GBP",or "CAD"
    """
    url = f"{API_ROOT}/users/me"
    data = {"ui_configuration": {"display_currency": {"code": code}}}
    x = session.put(url, json=data)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()
