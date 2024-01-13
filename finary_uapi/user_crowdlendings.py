import json
import logging
from typing import Dict, Union
import requests
from .constants import API_ROOT
from .user_holdings_accounts import (
    get_holdings_account_per_name_or_id,
    add_holdings_account,
)

CROWDLENDINGS_URL = f"{API_ROOT}/users/me/crowdlendings"


def get_user_crowdlendings(session: requests.Session):
    x = session.get(CROWDLENDINGS_URL)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def delete_user_crowdlending(session: requests.Session, crowdlending_id):
    """
    crowdlending_id is the numerical id of the crowdlending for this user, as provided by GET
    """
    url = f"{CROWDLENDINGS_URL}/{crowdlending_id}"
    x = session.delete(url)
    logging.debug(x.status_code)
    return x.status_code


def add_user_crowdlending(
    session: requests.Session,
    account_id: str,
    annual_yield: float,
    currency_code: str,
    current_price: float,
    initial_investment: float,
    month_duration: int,
    name: str,
    start_date: str,
):
    """
    `start_date` is of format "%a %b %d %Y %H:%M:%S GMT%z (%Z)"
    Tue Dec 26 2023 01:00:00 GMT+0100 (heure normale d’Europe centrale)
    """
    data: Dict[str, Union[str, float, int, Dict[str, str]]] = {}
    data["account"] = {"id": account_id}
    data["annual_yield"] = annual_yield
    data["currency"] = {"code": currency_code}
    data["current_price"] = current_price
    data["initial_investment"] = initial_investment
    data["month_duration"] = month_duration
    data["name"] = name
    data["start_date"] = start_date
    data_json = json.dumps(data)
    print(data_json)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.post(CROWDLENDINGS_URL, data=data_json, headers=headers)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


# convenience functions


def add_user_crowdlending_to_account(
    session: requests.Session,
    account_name: str,
    annual_yield: float,
    currency_code: str,
    current_price: float,
    initial_investment: float,
    month_duration: int,
    name: str,
    start_date: str,
):
    """
    `account_name` is the name of the account. If it doesn't exist, it will be created
    `start_date` format is YYYY-MM-DD (2023-12-24)
    """
    holdings_account_id = ""
    account = get_holdings_account_per_name_or_id(session, account_name, "crowdlending")
    if not account:
        account = add_holdings_account(
            session, account_name, "crowdlending", currency_code
        )
        account = account["result"]
    holdings_account_id = account["id"]

    return add_user_crowdlending(
        session,
        holdings_account_id,
        annual_yield,
        currency_code,
        current_price,
        initial_investment,
        month_duration,
        name,
        start_date,
    )
