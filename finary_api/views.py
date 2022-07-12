import json
import logging
import requests
from .constants import API_ROOT
from .utils import get_and_print

views_url = f"{API_ROOT}/users/me/views"
a_period = ["all", "1w", "1m", "ytd", "1y"]
a_dashboard_type = ["gross", "net", "finary"]


def get_period_view(session: requests.Session, url: str, period: str):
    """
    `period` can be "all", "1w", "1m", "ytd", "1y", it not specified, Finary will use "all"
    """
    params = {}
    if period:
        params["period"] = period
    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def get_dashboard(session: requests.Session, type: str, period: str):
    """
    `type` is required and can be "net", "gross", "finary"
    `period` can be "all", "1w", "1m", "ytd", "1y", it not specified, Finary will use "all"
    """
    url = f"{views_url}/dashboard"
    params = {}
    if type:
        params["type"] = type
    if period:
        params["period"] = period
    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def get_portfolio(session: requests.Session, period: str):
    """
    `period` can be "all", "1w", "1m", "ytd", "1y", it not specified, Finary will use "all"
    """
    url = f"{views_url}/portfolio"
    return get_period_view(session, url, period)


def get_savings_accounts(session: requests.Session, period: str):
    """
    `period` can be "all", "1w", "1m", "ytd", "1y", it not specified, Finary will use "all"
    """
    url = f"{views_url}/savings_accounts"
    return get_period_view(session, url, period)


def get_checking_accounts(session: requests.Session, period: str):
    """
    `period` can be "all", "1w", "1m", "ytd", "1y", it not specified, Finary will use "all"
    """
    url = f"{views_url}/checking_accounts"
    return get_period_view(session, url, period)


def get_other_assets(session: requests.Session, period: str):
    """
    `period` can be "all", "1w", "1m", "ytd", "1y", it not specified, Finary will use "all"
    """
    url = f"{views_url}/other_assets"
    return get_period_view(session, url, period)


def get_fonds_euro(session: requests.Session, period: str):
    """
    `period` can be "all", "1w", "1m", "ytd", "1y", it not specified, Finary will use "all"
    """
    url = f"{views_url}/fonds_euro"
    return get_period_view(session, url, period)


def get_real_estates(session: requests.Session, period: str):
    """
    `period` can be "all", "1w", "1m", "ytd", "1y", it not specified, Finary will use "all"
    """
    url = f"{views_url}/real_estates"
    return get_period_view(session, url, period)


def get_commodities(session: requests.Session, period: str):
    """
    `period` can be "all", "1w", "1m", "ytd", "1y", it not specified, Finary will use "all"
    """
    url = f"{views_url}/commodities"
    return get_period_view(session, url, period)


def get_insights(session: requests.Session):
    url = f"{views_url}/insights"
    return get_and_print(session, url)


def get_fees(session: requests.Session):
    url = f"{views_url}/fees"
    return get_and_print(session, url)


def get_loans(session: requests.Session):
    url = f"{views_url}/loans"
    return get_and_print(session, url)
