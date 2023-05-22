import json
import logging
import requests

from .utils import get_and_print
from .constants import API_ROOT

GENERIC_ASSET_ROOT = f"{API_ROOT}/users/me/generic_assets"


def get_user_generic_assets(session: requests.Session):
    return get_and_print(session, GENERIC_ASSET_ROOT)


def add_user_generic_asset(
    session: requests.Session, name, category, quantity, buying_price, current_price
):
    """
    category must be a string as returned by generic_assets_categories
    """
    url = GENERIC_ASSET_ROOT
    data = {}
    data["name"] = name
    data["category"] = category
    data["quantity"] = quantity
    data["buying_price"] = buying_price
    data["current_price"] = current_price
    data_json = json.dumps(data)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.post(url, data=data_json, headers=headers)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def update_user_generic_asset(
    session: requests.Session,
    asset_id,
    name,
    category,
    quantity,
    buying_price,
    current_price,
):
    url = f"{GENERIC_ASSET_ROOT}/{asset_id}"
    data = {}
    data["name"] = name
    data["category"] = category
    data["quantity"] = quantity
    data["buying_price"] = buying_price
    data["current_price"] = current_price
    data["id"] = asset_id
    data_json = json.dumps(data)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.put(url, data=data_json, headers=headers)
    logging.debug(x.status_code)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def delete_user_generic_asset(session: requests.Session, asset_id):
    """
    `asset_id` is the id of the asset for this user, as provided by GET
    """
    url = f"{GENERIC_ASSET_ROOT}/{asset_id}"
    x = session.delete(url)
    logging.debug(x.status_code)
    return x.status_code
