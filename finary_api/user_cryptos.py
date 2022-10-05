import json
import logging
import requests
from .constants import API_ROOT
from .currencies import get_cryptocurrency_by_code


def get_user_cryptos(session: requests.Session):
    url = f"{API_ROOT}/users/me/cryptos"
    x = session.get(url)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def delete_user_crypto(session: requests.Session, crypto_id):
    """
    crypto_id is the numerical id of the crypto for this user, as provided by GET
    """
    url = f"{API_ROOT}/users/me/cryptos/{crypto_id}"
    x = session.delete(url)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def add_user_crypto(
    session: requests.Session,
    correlation_id,
    quantity,
    buying_price,
    holdings_account_id,
):
    """
    correlation_id is a correlation id as send back by the currencies API (currencies.py)
    holdings_account_id is the id of the account the crypto will be added too
    """
    url = f"{API_ROOT}/users/me/cryptos"
    data = {}
    data["quantity"] = quantity
    data["buying_price"] = buying_price
    data["correlation_id"] = correlation_id
    data["holdings_account"] = {"id": holdings_account_id}
    data_json = json.dumps(data)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.post(url, data=data_json, headers=headers)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def update_user_crypto(session: requests.Session, crypto, quantity, buying_price):
    """
    crypto is a crypto dict as provided by GET
    """
    crypto_id = crypto["id"]
    crypto["quantity"] = quantity
    crypto["buying_price"] = buying_price
    url = f"{API_ROOT}/users/me/cryptos/{crypto_id}"
    crypto_json = json.dumps(crypto)
    headers = {}
    headers["Content-Length"] = str(len(crypto_json))
    headers["Content-Type"] = "application/json"
    x = session.put(url, data=crypto_json, headers=headers)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


# convenience functions


def add_user_crypto_by_code(
    session: requests.Session, crypto_code, quantity, buying_price, holdings_account_id
):
    """
    Search for a crypto by code and add it for a user
    crypto_code is ETH, BTC etc...
    """
    if currency := get_cryptocurrency_by_code(session, crypto_code):
        correlation_id = currency["correlation_id"]
        return add_user_crypto(
            session, correlation_id, quantity, buying_price, holdings_account_id
        )
    else:
        logging.info(f"Crypto currency [{crypto_code}] not found")
        return {}


def get_user_crypto_by_code(
    session: requests.Session, crypto_code, holdings_account_id
):
    user_cryptos = get_user_cryptos(session)
    user_crypto = {}
    for crypto in user_cryptos["result"]:
        if (
            crypto["crypto"]["code"] == crypto_code
            and crypto["account"]["id"] == holdings_account_id
        ):
            logging.debug(crypto)
            user_crypto = crypto
            break
    return user_crypto


def update_user_crypto_by_code(
    session: requests.Session, crypto_code, quantity, buying_price, holdings_account_id
):
    """
    Get user cryptos, find the one corresponding to crypto_code and update it
    with quantity and buying price. Add new crypto if not found
    """
    user_crypto = get_user_crypto_by_code(session, crypto_code, holdings_account_id)
    if user_crypto:
        return update_user_crypto(session, user_crypto, quantity, buying_price)
    else:
        return add_user_crypto_by_code(
            session, crypto_code, quantity, buying_price, holdings_account_id
        )


def delete_user_crypto_by_code(
    session: requests.Session, crypto_code, holdings_account_id
):
    """
    Get user cryptos, find the one corresponding to crypto_code and delete it
    """
    crypto = get_user_crypto_by_code(session, crypto_code, holdings_account_id)
    if crypto:
        return delete_user_crypto(session, crypto["id"])
