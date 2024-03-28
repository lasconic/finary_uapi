import json
import logging
import httpx
from .constants import API_ROOT


def get_bank_account_types(session: httpx.Client, type: str):
    """
    type = 'invest' (securities) or 'cash' (bank_accounts)
    """
    url = f"{API_ROOT}/bank_account_types"
    params = {}
    if type:
        params["type"] = type
    x = session.get(url, params=params)
    logging.debug(json.dumps(x.json(), indent=4))
    return x.json()


# utils functions
def get_bank_account_type_per_name(session: httpx.Client, type: str, name: str):
    accounts = get_bank_account_types(session, type)
    for a in accounts["result"]:
        if a["display_name"] == name:
            return a
    return {}
