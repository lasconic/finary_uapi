import json
import logging
import httpx
from .constants import API_ROOT
from .precious_metals import get_precious_metals


def get_user_precious_metals(session: httpx.Client):
    url = f"{API_ROOT}/users/me/precious_metals"
    x = session.get(url)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def add_user_precious_metals(
    session: httpx.Client, precious_metal_id, quantity, buying_price
):
    url = f"{API_ROOT}/users/me/precious_metals"
    data = {}
    data["quantity"] = quantity
    data["buying_price"] = buying_price
    data["precious_metal"] = {"id": precious_metal_id}
    x = session.post(url, json=data)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


def add_user_precious_metals_by_name(
    session: httpx.Client, name, quantity, buying_price
):
    metals = get_precious_metals(session, name)
    if metals and metals["result"]:
        precious_metal_id = metals["result"][0]["id"]
        return add_user_precious_metals(
            session, precious_metal_id, quantity, buying_price
        )
    return {}


def delete_user_precious_metals(session: httpx.Client, user_precious_metal_id):
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
