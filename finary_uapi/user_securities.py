import json
import logging
import requests
from .constants import API_ROOT
from .securities import get_securities, guess_security
from .user_holdings_accounts import (
    get_holdings_account_per_name_or_id,
    add_holdings_account,
)


def get_user_securities(session: requests.Session):
    url = f"{API_ROOT}/users/me/securities"
    x = session.get(url)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def add_user_security(
    session: requests.Session,
    holdings_account_id,
    correlation_id,
    quantity,
    buying_price,
):
    url = f"{API_ROOT}/users/me/securities"
    data = {}
    data["holdings_account"] = {"id": holdings_account_id}
    data["buying_price"] = buying_price
    data["correlation_id"] = correlation_id
    data["quantity"] = quantity
    data_json = json.dumps(data)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.post(url, data=data_json, headers=headers)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def update_user_security(
    session: requests.Session, security, quantity, buying_price, account_id
):
    url = f"{API_ROOT}/users/me/securities/{security['id']}"
    data = {}
    # data["bank_account_type"] = {id:""}
    data["quantity"] = quantity
    data["buying_price"] = buying_price
    data["symbol"] = security["security"]
    data["holdings_account"] = {"id": account_id}
    data_json = json.dumps(data)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.put(url, data=data_json, headers=headers)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def delete_user_security(session: requests.Session, security_id):
    """
    `security_id` is the id of the asset for this user, as provided by GET
    """
    url = f"{API_ROOT}/users/me/securities/{security_id}"
    x = session.delete(url)
    logging.debug(x.status_code)
    return x.status_code


# convenience functions


def add_user_security_by_symbol(
    session: requests.Session, symbol, holdings_account_id, quantity, buying_price
):
    securities = get_securities(session, symbol)
    if securities["result"]:
        correlation_id = securities["result"][0]["correlation_id"]
        return add_user_security(
            session,
            holdings_account_id,
            correlation_id,
            quantity,
            buying_price,
        )
    else:
        logging.warn("Symbol not found")
    return {}


def add_user_security_by_symbol_to_account(
    session: requests.Session, symbol, account_name, quantity, buying_price
):
    """ """
    holdings_account_id = ""
    if account := get_holdings_account_per_name_or_id(session, account_name):
        holdings_account_id = account["id"]
        return add_user_security_by_symbol(
            session, symbol, holdings_account_id, quantity, buying_price
        )
    else:
        logging.warn("Account not found")
        return {}


def add_user_security_to_account(
    session: requests.Session, security, account_name, quantity, buying_price
):
    """
    security is a json object as returned by get
    """
    holdings_account_id = ""
    if account := get_holdings_account_per_name_or_id(session, account_name):
        holdings_account_id = account["id"]
        return add_user_security(
            session,
            holdings_account_id,
            security["correlation_id"],
            quantity,
            buying_price,
        )
    else:
        logging.warn("Account not found")
        return {}


def add_imported_securities_to_account(
    session: requests.Session,
    account_name_id: str,
    to_be_imported,
    edit=False,
    delete=False,
    dry_run=False,
):
    """
    `account_name_id` is a name or an id
    `to_be_imported` in array of dict as defined in the import folder for stocks
    The function will try to find the account and create if not found.
    Then add the securities, and so add to them if they exist
    If `edit` is True, it will edit the security instead of adding to it,
    it will create the security line if not found. It doesn't delete securities!
        * If `dry_run` is True, it will do nothing but log what it would do
    """
    account = get_holdings_account_per_name_or_id(session, account_name_id)
    if not account:
        account = add_holdings_account(session, account_name_id, "stocks")
        account = account["result"]

    if edit:
        for account_security in account["securities"]:
            found = False
            for line in to_be_imported:
                if account_security["security"]["isin"] == line["isin_code"]:
                    found = True
                    break
            if not found:
                if dry_run:
                    logging.info(f'-- Delete {account_security["security"]["name"]}')

    for line in to_be_imported:
        # search by ISIN in the account
        security = {}
        for account_security in account["securities"]:
            if account_security["security"]["isin"] == line["isin_code"]:
                security = account_security["security"]
                break
        # if not found, try to guess
        if not security:
            security = guess_security(session, line)
        if security:
            if edit:
                found = False
                for account_security in account["securities"]:
                    if (
                        security["correlation_id"]
                        == account_security["security"]["correlation_id"]
                    ):
                        if (
                            line["quantity"] != account_security["quantity"]
                            or line["price"] != account_security["display_buying_price"]
                        ):
                            if dry_run:
                                logging.info(
                                    f'** Update [{security["name"]}]: {account_security["quantity"]} -> {line["quantity"]} - [{account_security["display_buying_price"]} -> {line["price"]}]'  # noqa
                                )
                            else:
                                update_user_security(
                                    session,
                                    account_security,
                                    line["quantity"],
                                    line["price"],
                                    account["id"],
                                )
                        found = True
                        break
                if not found:
                    if dry_run:
                        logging.info(
                            f'++ Add [{security["symbol"]}]: {line["quantity"]} - {line["price"]}'  # noqa
                        )
                    else:
                        add_user_security(
                            session,
                            account["id"],
                            security["correlation_id"],
                            line["quantity"],
                            line["price"],
                        )
            else:
                if dry_run:
                    logging.info(
                        f'+ Add [{security["symbol"]}]: {line["quantity"]} - {line["price"]}'
                    )
                else:
                    add_user_security(
                        session,
                        account["id"],
                        security["correlation_id"],
                        line["quantity"],
                        line["price"],
                    )
