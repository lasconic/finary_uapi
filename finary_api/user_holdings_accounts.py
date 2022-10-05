import json
import logging
from typing import Any, Dict
import requests

from .constants import API_ROOT
from .institutions import get_institutions
from .bank_account_types import get_bank_account_type_per_name

holdings_accounts_url = f"{API_ROOT}/users/me/holdings_accounts"


def add_holdings_account(
    session: requests.Session,
    name: str,
    type: str,
    currency: str = "USD",
    bank_account_type={},
    institution={},
    balance=None,
):
    """
    type can be "crypto" or "stocks"
    #TODO currency code seems to be an old API, maybe replace by currency_id
    """
    url = holdings_accounts_url
    data: Dict[str, Any] = {}
    data["name"] = name
    if type:
        data["manual_type"] = type
    data["currency"] = {"code": currency}
    if bank_account_type:
        data["bank_account_type"] = bank_account_type
    if institution:
        data["institution"] = institution
    if balance is not None:
        data["balance"] = balance
    data_json = json.dumps(data)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.post(url, data=data_json, headers=headers)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def get_holdings_accounts(session: requests.Session, type: str = ""):
    """
    type can be "crypto" or "stocks", or empty for all accounts
    """
    url = holdings_accounts_url
    params = {}
    if type:
        params["manual_type"] = type
    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def delete_holdings_account(session: requests.Session, account_id: str):
    """
    account_id is the alphanumeric id of the account, as provided by GET
    """
    url = f"{holdings_accounts_url}/{account_id}"
    x = session.delete(url)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def update_holdings_account(
    session: requests.Session, account_id: str, name: str, balance=None
):
    """
    account_id is the alphanumeric id of the account, as provided by GET
    """
    url = f"{holdings_accounts_url}/{account_id}"
    data = {}
    data["name"] = name
    if balance is not None:
        data["balance"] = balance
    data_json = json.dumps(data)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.put(url, data=data_json, headers=headers)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


# convenience functions
def get_holdings_account_per_name_or_id(session: requests.Session, name):
    accounts = get_holdings_accounts(session)
    for a in accounts["result"]:
        if a["name"] == name or a["id"] == name:
            return a
    return {}


def add_checking_saving_account(
    session: requests.Session,
    account_name: str,
    institution_name: str,
    account_type: str,
    balance: float,
):
    # TODO currency
    institutions = get_institutions(session, institution_name)
    if institutions and "result" in institutions:
        institution = institutions["result"][0]
    else:
        logging.error(f"Can't find institution : [{institution_name}]")
        return {}
    bank_account_type = get_bank_account_type_per_name(session, "cash", account_type)
    if not bank_account_type:
        logging.error(f"Can't find bank account type : [{account_type}]")
        return {}
    return add_holdings_account(
        session,
        account_name,
        "",
        bank_account_type=bank_account_type,
        institution=institution,
        balance=balance,
    )
