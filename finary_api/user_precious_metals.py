import json
import logging
import requests
from .constants import API_ROOT
from .precious_metals import get_precious_metals


def get_user_precious_metals(session: requests.Session):
    url = f"{API_ROOT}/users/me/precious_metals"
    x = session.get(url)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def add_user_precious_metals(
    session: requests.Session, precious_metal_id, quantity, buying_price
):
    url = f"{API_ROOT}/users/me/precious_metals"
    data = {}
    data["quantity"] = quantity
    data["buying_price"] = buying_price
    data["precious_metal"] = {"id": precious_metal_id}
    data_json = json.dumps(data)
    headers = {}
    headers["Content-Length"] = str(len(data_json))
    headers["Content-Type"] = "application/json"
    x = session.post(url, data=data_json, headers=headers)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def add_user_precious_metals_by_name(
    session: requests.Session, name, quantity, buying_price
):
    metals = get_precious_metals(session, name)
    if metals and metals["result"]:
        precious_metal_id = metals["result"][0]["id"]
        return add_user_precious_metals(
            session, precious_metal_id, quantity, buying_price
        )
    return {}


def delete_user_precious_metals(session: requests.Session, user_precious_metal_id):
    """
    user_precious_metal_id is the id of the line for the given user,
    """
    url = f"{API_ROOT}/users/me/precious_metals/{user_precious_metal_id}"
    x = session.delete(url)
    logging.debug(x.status_code)
    # TODO no json return yet... maybe one day ?
    # logging.debug(x.text)
    # logging.debug(json.dumps(x.json(), indent=4))
    return x.status_code


# TODO update, apparently it's possible to update not only quantity and price,
# but also the type of metal, to be investigated.
