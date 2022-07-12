import json
import logging
import requests

from .constants import API_ROOT
from .utils import get_and_print

portfolio_api = f"{API_ROOT}/users/me/portfolio"


def get_portfolio(session: requests.Session, portfolio_type: str):
    """
    portfolio_type is "investments" or "cryptos"
    """
    url = f"{portfolio_api}/{portfolio_type}"
    return get_and_print(session, url)


def get_portfolio_cryptos(session: requests.Session):
    return get_portfolio(session, "cryptos")


def get_portfolio_cryptos_distribution(session: requests.Session):
    return get_portfolio_distribution(session, "cryptos", "crypto")


def get_portfolio_investments(session: requests.Session):
    return get_portfolio(session, "investments")


def get_portfolio_timeseries(
    session: requests.Session, portfolio_type: str, period: str, type: str
):
    """
    `portfolio_type` is "investments" or "cryptos"
    `period` can be "all", "1w", "1m", "ytd", "1y", it not specified, Finary will use "all"
    """
    url = f"{portfolio_api}/{portfolio_type}/timeseries"
    params = {}
    if period:
        params["period"] = period
    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def get_portfolio_distribution(
    session: requests.Session, portfolio_type: str, type: str
):
    """
    portfolio_type is "investments" or "cryptos"
    type is "crypto" or "stock" or "sector" (all ?)
    """
    url = f"{portfolio_api}/{portfolio_type}/distribution"
    params = {}
    if type:
        params["type"] = type
    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()
