import json
import logging
from .constants import API_ROOT
from curl_cffi import requests
from .utils import get_and_print
from .user_holdings_accounts import (
    get_holdings_account_per_name_or_id,
    add_holdings_account,
)

def get_user_fonds_euro(session: requests.Session):
    fe_url = f"{API_ROOT}/users/me/fonds_euro"
    return get_and_print(session, fe_url)


def add_user_fonds_euro(session: requests.Session, bank, name, buying_price):
    url = f"{API_ROOT}/users/me/fonds_euro"
    print(url)
    data = {}
    #data["annual_yield"] = annual_yield
    data["bank"] = bank
    data["current_price"] = buying_price
    data["buying_price"] = buying_price
    data["name"] = name
    data_json = json.dumps(data)
    print(data_json)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.post(url, data=data_json, headers=headers)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()

def update_user_fonds_euro(session: requests.Session, fond, current_price):
    url = f"{API_ROOT}/users/me/fonds_euro/{fond['id']}"
    data = {}
    #data["annual_yield"] = annual_yield
    data["current_price"] = current_price
    #data["buying_price"] = buying_price
    data_json = json.dumps(data)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.put(url, data=data_json, headers=headers)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()

def delete_user_fonds_euro(session: requests.Session, fond_id):
    url = f"{API_ROOT}/users/me/fonds_euro/{fond_id}"
    x = session.delete(url)
    logging.debug(x.status_code)
    return x.status_code

def add_imported_fonds_euro_to_account(session: requests.Session, account_name_id: str, to_be_imported, edit=False, delete=False, dry_run=False):
    account = get_holdings_account_per_name_or_id(session, account_name_id)
    if not account:
        account = add_holdings_account(session, account_name_id, "stocks")
        account = account["result"]

    if edit:
        for fonds_euro in account["fonds_euro"]:
            found = False
            for line in to_be_imported:
                if fonds_euro["name"] == line["description"]:
                    found = True
                    break
            if not found:
                logging.info(f'-- Delete {fonds_euro["name"]}')
                if not dry_run:
                    delete_user_fonds_euro(session, fonds_euro["id"])

    for line in to_be_imported:
        if edit:
            found = False
            for fonds_euro in account["fonds_euro"]:
                if (
                    line["description"]
                    == fonds_euro["name"]
                ):
                    if (
                        line["price"] != fonds_euro["current_price"]
                        ):
                        logging.info(
                            f'** Update [{line["description"]}]: [{fonds_euro["current_price"]} -> {line["price"]}]'  # noqa
                        )
                        if not dry_run:
                            update_user_fonds_euro(
                                session,
                                fonds_euro,
                                line["price"],
                            )
                    found = True
                    break
            if not found:
                logging.info(
                    f'++ Add [{line["description"]}]: {line["price"]}'  # noqa
                )
                if not dry_run:
                    add_user_fonds_euro(
                        session,
                        account["bank"],
                        line["description"],
                        line["price"],
                    )
        else:
            logging.info(
                f'+ Add [{line["description"]}]: {line["price"]}'
            )
            if not dry_run:
                add_user_fonds_euro(
                    session,
                    account["bank"],
                    line["description"],
                    line["price"],
                )