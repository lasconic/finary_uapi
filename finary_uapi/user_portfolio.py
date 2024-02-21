import json
import logging
import requests
from typing import Dict, Union

from .constants import API_ROOT
from .utils import get_and_print

portfolio_api = f"{API_ROOT}/users/me/portfolio"


def get_portfolio(session: requests.Session, portfolio_type: str):
    """
    portfolio_type is "investments", "cryptos", "crowdlendings"
    """
    url = f"{portfolio_api}/{portfolio_type}"
    return get_and_print(session, url)


def get_portfolio_crowdlendings(session: requests.Session):
    return get_portfolio(session, "crowdlendings")


def get_portfolio_crowdlendings_distribution(session: requests.Session):
    return get_portfolio_distribution(session, "crowdlendings", "account")


def get_portfolio_cryptos(session: requests.Session):
    return get_portfolio(session, "cryptos")


def get_portfolio_cryptos_distribution(session: requests.Session):
    return get_portfolio_distribution(session, "cryptos", "crypto")


def get_portfolio_investments(session: requests.Session):
    return get_portfolio(session, "investments")


def get_portfolio_timeseries(session: requests.Session, period: str, type: str):
    """
    `period` can be "all", "1w", "1m", "ytd", "1y". If not specified, Finary will use "all"
    `type` can be "gross", "net", "finary" (aka financial)
    """
    url = f"{portfolio_api}/timeseries"
    params = {}
    if type:
        params["type"] = type
    if period:
        params["period"] = period
    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def get_portfolio_distribution(
    session: requests.Session, portfolio_type: str, type: str
):
    """
    `portfolio_type` is "investments", "cryptos" or "crowdlendings"
    `type` is "crypto" or "stock" or "sector" or "account" (all ?)
    """
    url = f"{portfolio_api}/{portfolio_type}/distribution"
    params = {}
    if type:
        params["type"] = type
    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def get_portfolio_investments_dividends(session: requests.Session):
    portfolio_type = "investments"
    url = f"{portfolio_api}/{portfolio_type}/dividends"
    return get_and_print(session, url)


def get_portfolio_transactions(
    session: requests.Session,
    portfolio_type: str = "checking_accounts",
    page: int = 1,
    per_page: int = 50,
    query: str = "",
    account_id: str = "",
    institution_id: str = "",
):
    """
    `portfolio_type` is  "investments", "checking_accounts", "credit_accounts"
    """
    url = f"{portfolio_api}/{portfolio_type}/transactions"
    params: Dict[str, Union[str, int]] = {}
    params["page"] = page
    params["per_page"] = per_page
    if query:
        params["query"] = query
    if account_id:
        params["account_id"] = account_id
    if institution_id:
        params["institution_id"] = institution_id
    x = session.get(url, params=params)
    return x.json()


def get_portfolio_checking_accounts_transactions(
    session: requests.Session,
    page: int = 1,
    per_page: int = 50,
    query: str = "",
    account_id: str = "",
    institution_id: str = "",
):
    portfolio_type = "checking_accounts"
    return get_portfolio_transactions(
        session, portfolio_type, page, per_page, query, account_id, institution_id
    )


def get_portfolio_credit_accounts_transactions(
    session: requests.Session,
    page: int = 1,
    per_page: int = 50,
    query: str = "",
    account_id: str = "",
    institution_id: str = "",
):
    portfolio_type = "credit_accounts"
    return get_portfolio_transactions(
        session, portfolio_type, page, per_page, query, account_id, institution_id
    )


def get_portfolio_investments_transactions(
    session: requests.Session,
    page: int = 1,
    per_page: int = 50,
    query: str = "",
    account_id: str = "",
    institution_id: str = "",
):
    portfolio_type = "investments"
    return get_portfolio_transactions(
        session, portfolio_type, page, per_page, query, account_id, institution_id
    )
